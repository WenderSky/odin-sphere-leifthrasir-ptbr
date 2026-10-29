#!/usr/bin/env python3
# Licença: GNU GPL v2 (usa o cpk.py do projeto dragons-crown-pro-pc / odin-sphere-leifthrasir-pc).
"""Instalador da tradução PT-BR de Odin Sphere: Leifthrasir (PC Recomp).
Compatível com Windows e Steam Deck / Linux (utiliza apenas biblioteca padrão do Python).

    patcher.py apply  [caminho_jogo] [pasta_traducao]   instala ou atualiza a tradução
    patcher.py revert [caminho_jogo]                    restaura os arquivos originais
    patcher.py status [caminho_jogo]                    informa o status da instalação

caminho_jogo pode ser a pasta do port (onde fica o odin_sphere_leifthrasir.exe ou o AppImage), a pasta game,
game/prepared, a pasta de uma versão (CUSA05262-1.01...) ou um dos .CPK. Sem ele, o patcher procura sozinho.

Os textos traduzidos são anexados ao fim dos CPKs e o índice (TOC) passa a apontar para eles; nada dos dados
originais é sobrescrito. O registro de desfazer fica em <CPK>.ptbr.undo. O nome é diferente do <CPK>.undo do
launcher de propósito: o launcher trata a existência daquele arquivo como "botões de Xbox instalados".
"""

import hashlib
import os
import re
import shutil
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import cpk as cpklib

# Europa (CUSA05262) e EUA (CUSA05083). A versão japonesa não tem os textos em inglês.
REGIONS = ('UK', 'US')
UNDO_SUFFIX = '.ptbr.undo'
UNDO_MAGIC = b'OSLUNDO1'
LAUNCHER_UNDO_SUFFIX = '.undo'
LAUNCHER_UNDO_MAGIC = b'DCPUNDO1'
FONT_PATCH_MAGIC = b'OSLFTXP1'
PREPARED_MARKER = '.osl_view.json'


def archives(region):
    """(RE, BT, OR) da região."""
    return tuple(f'Odin2_{kind}_{region}.CPK' for kind in ('RE', 'BT', 'OR'))

# ------------------------------------------------------------------ Registro de Desfazer

def undo_path(cpk_path: Path) -> Path:
    return cpk_path.with_name(cpk_path.name + UNDO_SUFFIX)

def write_undo(path: Path, rec: dict):
    names = '\n'.join(rec['names']).encode('utf-8')
    path.write_bytes(UNDO_MAGIC
                     + struct.pack('<QQI', rec['original_len'], rec['toc_pos'], len(rec['toc'])) + rec['toc']
                     + struct.pack('<QI', rec['header_pos'], len(rec['header'])) + rec['header']
                     + struct.pack('<I', len(names)) + names)

def read_undo(path: Path) -> dict:
    """Lê o registro da tradução ou o do launcher (mesmo formato, outra assinatura)."""
    b = path.read_bytes()
    if b[:8] not in (UNDO_MAGIC, LAUNCHER_UNDO_MAGIC):
        raise ValueError(f'{path.name}: registro de desfazer invalido')
    original_len, toc_pos, toc_len = struct.unpack_from('<QQI', b, 8)
    pos = 28
    toc = b[pos:pos + toc_len]; pos += toc_len
    header_pos, header_len = struct.unpack_from('<QI', b, pos); pos += 12
    header = b[pos:pos + header_len]; pos += header_len
    names = []
    if pos + 4 <= len(b):
        n = struct.unpack_from('<I', b, pos)[0]
        names = [x for x in b[pos + 4:pos + 4 + n].decode('utf-8', 'replace').split('\n') if x]
    return dict(original_len=original_len, toc_pos=toc_pos, toc=toc, header_pos=header_pos, header=header,
                names=names)

def restore(cpk_file: Path, rec: dict):
    with open(cpk_file, 'r+b') as f:
        f.seek(rec['toc_pos'])
        f.write(rec['toc'])
        f.seek(rec['header_pos'])
        f.write(rec['header'])
        f.truncate(rec['original_len'])

def current_bytes(cpk_file: Path, pos: int, length: int) -> bytes:
    with open(cpk_file, 'rb') as f:
        f.seek(pos)
        return f.read(length)

def is_installed(cpk_file: Path, rec: dict) -> bool:
    size = cpk_file.stat().st_size
    return size > rec['original_len'] and current_bytes(cpk_file, rec['toc_pos'], len(rec['toc'])) != rec['toc']

def launcher_on_top(cpk_file: Path, rec: dict) -> bool:
    """O launcher aplicou os botões de Xbox depois da tradução: o registro dele parte de um arquivo já traduzido."""
    lu = cpk_file.with_name(cpk_file.name + LAUNCHER_UNDO_SUFFIX)
    if not lu.exists():
        return False
    try:
        return read_undo(lu)['original_len'] > rec['original_len']
    except (ValueError, struct.error):
        return False

# ------------------------------------------------------------------ Localizar o Jogo

def game_region(folder: Path):
    for region in REGIONS:
        if (folder / archives(region)[0]).is_file():
            return region
    return None

def active_build(prepared: Path):
    """A versão que o launcher roda: entre as pastas preparadas por inteiro ("scope": "full" no .osl_view.json),
    a preparada por último (é o que o launcher faz). Sem marcador, a única pasta com os CPKs."""
    builds = [d for d in sorted(prepared.iterdir()) if d.is_dir() and game_region(d)] if prepared.is_dir() else []
    chosen, chosen_time = None, None
    for d in builds:
        marker = d / PREPARED_MARKER
        try:
            if not re.search(r'"scope"\s*:\s*"full"', marker.read_text(encoding='utf-8', errors='replace')):
                continue
            t = marker.stat().st_mtime
        except OSError:
            continue
        if chosen is None or t > chosen_time:   # empate: a primeira, como no launcher
            chosen, chosen_time = d, t
    return chosen or (builds[-1] if builds else None)

def find_game_folder(user_path=None) -> Path:
    if user_path:
        clean = str(user_path).strip().strip('\'"')
        if clean.startswith('file://'):
            clean = clean[7:]
        p = Path(clean).expanduser()
        if p.is_file():
            p = p.parent
        if game_region(p):
            return p
        for prepared in (p / 'game' / 'prepared', p / 'prepared', p):
            build = active_build(prepared)
            if build:
                return build
        for region in REGIONS:
            for match in p.rglob(archives(region)[0]):
                return match.parent
        return None

    roots = [SCRIPT_DIR.parent.parent, SCRIPT_DIR.parent.parent.parent, Path.cwd(),
             Path(r"E:\Recomps\Odin Sphere Leifthrasir PS4 ver")]
    # AppImage em pasta só de leitura: dados em $XDG_DATA_HOME/OdinSphereLeifthrasirPC
    xdg = os.environ.get('XDG_DATA_HOME') or str(Path.home() / '.local' / 'share')
    roots.append(Path(xdg) / 'OdinSphereLeifthrasirPC')
    # Pastas comuns no Steam Deck / Linux: ~/Games/<pasta do port>
    for base in (Path.home() / 'Games', Path.home() / 'games', Path.home() / 'Jogos'):
        if base.is_dir():
            roots.extend(sorted(d for d in base.iterdir() if d.is_dir()))
    for root in roots:
        build = active_build(root / 'game' / 'prepared')
        if build:
            return build
    return None

def locate_folder(user_path=None) -> Path:
    folder = find_game_folder(user_path)
    if folder:
        return folder
    print('Pasta do jogo nao encontrada' + (f' em: {user_path}' if user_path else ' nos locais padrao.'))
    if not sys.stdin or not sys.stdin.isatty():
        return None
    try:
        typed = input('Arraste aqui a pasta do jogo (onde fica o odin_sphere_leifthrasir.exe ou o AppImage) '
                      'e tecle Enter: ')
    except EOFError:
        return None
    folder = find_game_folder(typed) if typed.strip() else None
    if not folder:
        print(f'Erro: os arquivos do jogo (Odin2_RE_UK.CPK ou Odin2_RE_US.CPK) nao foram encontrados em: {typed}')
    return folder

def unshare(cpk_file: Path):
    try:
        links = os.stat(cpk_file).st_nlink
    except OSError:
        return
    if links <= 1:
        return
    print(f'{cpk_file.name} e um hard link; criando copia propria antes de modificar...')
    tmp = cpk_file.with_name(cpk_file.name + '.copy')
    shutil.copyfile(cpk_file, tmp)
    os.replace(tmp, cpk_file)

# ------------------------------------------------------------------ Fontes (ã, õ, Ã, Õ, Â)

def apply_font_patch(original: bytes, patch_file: Path):
    """Aplica um fontes/<fonte>.ftx.patch (blocos BC3 gerados pelo gerar_fontes.py) sobre a fonte original
    do jogo. Devolve None se a fonte do jogo não for a esperada."""
    b = patch_file.read_bytes()
    if b[:8] != FONT_PATCH_MAGIC:
        raise ValueError(f'{patch_file.name}: patch de fonte invalido')
    sha1 = b[8:28]
    size, count = struct.unpack_from('<II', b, 28)
    if len(original) != size or hashlib.sha1(original).digest() != sha1:
        return None
    out = bytearray(original)
    pos = 36
    for _ in range(count):
        off = struct.unpack_from('<I', b, pos)[0]
        out[off:off + 16] = b[pos + 4:pos + 20]
        pos += 20
    return bytes(out)

# ------------------------------------------------------------------ Conferir o formato dos textos

TEXT_BLOCK_RE = re.compile(rb'@TEXT\s*\(')

def same_shape(original: bytes, new: bytes, rel: str) -> bool:
    """O arquivo traduzido tem a mesma estrutura do arquivo do jogo do usuário (mesmo número de textos)? Protege
    contra uma versão do jogo com textos diferentes daqueles em que a tradução foi feita."""
    if rel.endswith('.fms'):
        return (original[:4] == new[:4] == b'FMSB' and len(original) >= 24 and len(new) >= 24
                and original[20:24] == new[20:24])
    if rel.startswith('classic/'):
        return original[:64] == new[:64] and original.count(b'\0') == new.count(b'\0')
    if rel.startswith('archiveviewer/'):
        return len(TEXT_BLOCK_RE.findall(original)) == len(TEXT_BLOCK_RE.findall(new))
    return True

# ------------------------------------------------------------------ Aplicar Tradução em CPK

def patch_single_cpk(cpk_file: Path, files_to_patch: dict, font_patches: dict = None, classic: bool = False) -> bool:
    unshare(cpk_file)
    undo = undo_path(cpk_file)
    rec = None
    if undo.exists():
        rec = read_undo(undo)
        if not is_installed(cpk_file, rec):
            # O arquivo foi reinstalado, ou o launcher o restaurou: o registro não vale mais.
            rec = None
        elif not launcher_on_top(cpk_file, rec):
            print(f'Atualizando traducao ja instalada em {cpk_file.name}...')
            restore(cpk_file, rec)
            rec = None
        # Com os botões de Xbox do launcher por cima, não dá para cortar o arquivo: os textos novos só são
        # anexados de novo e o registro original (anterior à tradução) é mantido.

    arc = cpklib.Cpk(cpk_file)
    try:
        targets = []
        skipped = []
        for e in arc.entries:
            ep = e['path'].lower()
            rel = ep if ep in files_to_patch else ('classic/' + ep if classic else None)
            p = files_to_patch.get(rel) if rel else None
            if p:
                data = p.read_bytes()
                if same_shape(arc.read(e), data, rel):
                    targets.append((e, data))
                else:
                    skipped.append(e['path'])
            elif font_patches and ep in font_patches:
                data = apply_font_patch(arc.read(e), font_patches[ep])
                if data is None:
                    print(f'Aviso: {e["path"]} do jogo e diferente do esperado; letras com til (ã, õ) ficarao '
                          f'sem a fonte nova.')
                else:
                    targets.append((e, data))

        if skipped:
            print(f'Aviso: {len(skipped)} arquivo(s) de {cpk_file.name} tem textos diferentes dos esperados e '
                  f'ficaram em ingles: ' + ', '.join(skipped[:10]) + (' ...' if len(skipped) > 10 else ''))
        if not targets:
            return True # Nada a aplicar neste CPK

        toc_pos = arc.toc_offset + 16
        header_pos = 16
        original_toc = arc.toc.packet_bytes()
        if rec is None:
            rec = dict(original_len=cpk_file.stat().st_size, toc_pos=toc_pos, toc=original_toc,
                       header_pos=header_pos, header=arc.header.packet_bytes(), names=[])
        rec['names'] = sorted(set(rec['names']) | {e['path'] for e, _ in targets})
        write_undo(undo, rec)

        align = arc.align or 0x800
        print(f'\nAplicando {len(targets)} arquivos em {cpk_file.name}:')
        with open(cpk_file, 'r+b') as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            for e, data in targets:
                pos = (pos + align - 1) // align * align
                f.seek(pos)
                f.write(data)
                row = e['row']
                arc.toc.set_number(row, 'FileOffset', pos - arc.toc_base)
                arc.toc.set_number(row, 'FileSize', len(data))
                if (row, 'ExtractSize') in arc.toc.positions:
                    arc.toc.set_number(row, 'ExtractSize', len(data))
                print(f'  [+] {e["path"]} ({len(data)} bytes)')
                pos += len(data)
            new_toc = arc.toc.packet_bytes()
            assert len(new_toc) == len(original_toc), 'o tamanho do TOC mudou'
            f.seek(toc_pos)
            f.write(new_toc)
            h = arc.header.rows[0]
            for flag in ('EnableTocCrc', 'EnableFileCrc'):
                if h.get(flag) and (0, flag) in arc.header.positions:
                    arc.header.set_number(0, flag, 0)
            f.seek(header_pos)
            f.write(arc.header.packet_bytes())
    finally:
        arc.f.close()

    # Verificação pós-patch
    check = cpklib.Cpk(cpk_file)
    try:
        bad = [e['path'] for e, data in targets if check.read(check.entries[e['row']]) != data]
    finally:
        check.f.close()
    if bad:
        print(f'Erro: verificacao falhou para {", ".join(bad)} em {cpk_file.name}; restaurando original.')
        restore(cpk_file, rec)
        undo.unlink()
        return False
    return True

def apply_translation(game_path, mod_dir):
    folder = locate_folder(game_path)
    if not folder:
        return False
    mod_dir = Path(mod_dir).resolve()
    all_mod_files = {}
    font_patches = {}
    for p in sorted(mod_dir.rglob('*')):
        if p.is_file():
            rel = p.relative_to(mod_dir).as_posix().lower()
            if rel.startswith('fontes/') and rel.endswith('.patch'):
                font_patches[rel[len('fontes/'):-len('.patch')]] = p
            else:
                all_mod_files[rel] = p

    if not all_mod_files:
        print(f'Erro: nenhum arquivo de traducao encontrado em {mod_dir}')
        return False

    region = game_region(folder)
    print(f'Pasta do jogo: {folder}')
    if region == 'US':
        print('Versao americana (CUSA05083): a traducao foi feita sobre a europeia; os arquivos com textos '
              'diferentes ficam em ingles.')
    re_cpk, bt_cpk, or_cpk = (folder / n for n in archives(region))

    success = patch_single_cpk(re_cpk, all_mod_files)
    if bt_cpk.exists():
        success = patch_single_cpk(bt_cpk, all_mod_files, font_patches) and success
    if or_cpk.exists():
        success = patch_single_cpk(or_cpk, all_mod_files, classic=True) and success

    if success:
        print('\n======================================================')
        print(' Traducao PT-BR de Odin Sphere instalada com sucesso!')
        print('======================================================')
    return success

def revert_translation(game_path):
    folder = locate_folder(game_path)
    if not folder:
        return False
    print(f'Pasta do jogo: {folder}')
    
    names = archives(game_region(folder))
    records = []
    for archive_name in names:
        cpk_file = folder / archive_name
        undo = undo_path(cpk_file)
        if cpk_file.exists() and undo.exists():
            records.append((cpk_file, undo, read_undo(undo)))

    blocked = [c.name for c, _, rec in records if is_installed(c, rec) and launcher_on_top(c, rec)]
    if blocked:
        print(f'Erro: os botoes de Xbox foram aplicados pelo launcher depois da traducao ({", ".join(blocked)}).\n'
              'No launcher, volte "Controller prompts" para PlayStation, rode o desinstalador de novo e depois '
              'escolha os botoes de Xbox outra vez, se quiser.')
        return False

    reverted_any = False
    for cpk_file, undo, rec in records:
        if is_installed(cpk_file, rec):
            print(f'Restaurando {cpk_file.name} original...')
            restore(cpk_file, rec)
            reverted_any = True
        undo.unlink()

    if reverted_any:
        print('\nSucesso! A traducao foi desinstalada e o jogo voltou ao original em ingles.')
    else:
        print('A traducao nao estava instalada.')
    return True

def status(game_path):
    folder = find_game_folder(game_path)
    if not folder:
        print('Pasta do jogo nao encontrada.')
        return False
    re_cpk = folder / archives(game_region(folder))[0]
    undo = undo_path(re_cpk)
    on = undo.exists() and is_installed(re_cpk, read_undo(undo))
    print(f'{folder}: traducao {"INSTALADA" if on else "nao instalada"}')
    return on

def main():
    try:
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ('apply', 'revert', 'restore', 'status'):
        print(__doc__)
        sys.exit(2)
    action = sys.argv[1].lower()
    game_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip() else None
    if action == 'apply':
        mod_dir = sys.argv[3] if len(sys.argv) > 3 else str(SCRIPT_DIR.parent / 'arquivos_traducao')
        ok = apply_translation(game_path, mod_dir)
    elif action in ('revert', 'restore'):
        ok = revert_translation(game_path)
    else:
        ok = status(game_path)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
