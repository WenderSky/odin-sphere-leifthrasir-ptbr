# 🔮 Odin Sphere: Leifthrasir (Recomp PC) — Tradução PT-BR

> Tradução **não-oficial** para **Português do Brasil** de *Odin Sphere: Leifthrasir* na versão **recompilada para PC / Steam Deck** ([saulob/odin-sphere-leifthrasir-pc](https://github.com/saulob/odin-sphere-leifthrasir-pc)).

<p align="center">
  <img alt="Idioma" src="https://img.shields.io/badge/idioma-Portugu%C3%AAs%20(BR)-009c3b">
  <img alt="Plataforma" src="https://img.shields.io/badge/plataforma-PC%20%2B%20Steam%20Deck-1b2838">
  <img alt="Versão" src="https://img.shields.io/badge/vers%C3%A3o-1.1-6a0dad">
  <img alt="Uso" src="https://img.shields.io/badge/uso-n%C3%A3o--comercial-important">
</p>

---

## 📜 Sobre

O recomp roda a versão de PS4 de *Odin Sphere: Leifthrasir* nativamente no PC e no Steam Deck. Esta tradução troca os textos em inglês do jogo pelo português do Brasil: história, menus, itens, habilidades, a biblioteca da Alice e até o Modo Clássico.

Basta manter o idioma do jogo em **English** (o padrão) — com a tradução instalada, ele aparece em português.

> ⚠️ **Aviso:** esta é uma **tradução amadora**, feita por um fã, e **pode conter erros** — typos, trechos com sentido ligeiramente diferente do original, ou alguma linha que fique apertada na caixa de texto. Não é um trabalho profissional/oficial. Se encontrar algum erro, abra uma [*issue*](../../issues) que eu corrijo em versões futuras. 🙂

### 🎯 Versões do jogo

| Versão | Situação |
|--------|----------|
| 🇪🇺 Europa — CUSA05262 (1.00 ou 1.01) | ✅ Testada |
| 🇺🇸 EUA — CUSA05083 | ⚠️ Deve funcionar, mas não foi testada. O instalador confere cada arquivo e deixa em inglês os que forem diferentes |
| 🇯🇵 Japão — CUSA01290 | ❌ Não suportada (não tem os textos em inglês) |

---

## 🎮 O que foi traduzido

**Cerca de 17 mil textos** em 461 arquivos do jogo:

| Parte do jogo | Textos |
|------|---------|
| 📖 Diálogos da história dos 5 personagens (Gwendolyn, Cornelius, Mercedes, Oswald e Velvet), prólogos, epílogos e descansos | 8.814 textos em 79 arquivos de mensagens |
| 🧭 Menus, interface, opções, mapas e tutoriais | *(incluídos acima)* |
| ✨ Habilidades Psypher, magias, itens, receitas de alquimia, sementes e pratos do Pooka Café e do restaurante | *(incluídos acima)* |
| 📚 Livros da biblioteca do sótão da Alice | 373 textos em 131 arquivos |
| 🕹️ Modo Clássico (o *Odin Sphere* original, incluído no Leifthrasir) | 7.857 textos em 251 arquivos |

### 🔤 Letras com til

A fonte do jogo não tinha **ã, õ, Ã, Õ** nem **Â**. O instalador desenha essas letras nas três fontes do jogo, no lugar de **ä, ö, Ä, Ö** e **Ñ** (que o português não usa), no mesmo estilo de cada fonte. O pacote só leva os pedaços da imagem que mudam (3 a 6 KB por fonte), aplicados sobre a fonte do seu próprio jogo.

> Efeito colateral: com a tradução instalada, os idiomas **alemão** e **espanhol** do jogo mostrariam til no lugar do trema e do Ñ. Desinstalar volta tudo ao original.

### 🚫 O que **não** foi traduzido

| Item | Por quê |
|------|---------|
| Textos desenhados em imagens (logos, títulos, alguns botões) | Ficam para uma versão futura |
| Nomes de personagens | Nomes próprios |
| Vozes | São áudio |

---

## 💾 Instalação

> **Requisitos:** o recomp do *Odin Sphere: Leifthrasir* já instalado e funcionando. O instalador usa **Python 3** — no **Steam Deck / Linux** já vem instalado; no **Windows**, se não tiver, baixe em [python.org/downloads](https://www.python.org/downloads/) marcando *"Add python.exe to PATH"*.

### 🪟 Windows

1. Baixe o `.zip` da [última versão](../../releases/latest) e **descompacte** (de preferência dentro da pasta do jogo — assim o instalador acha o jogo sozinho).
2. **Feche o jogo e o launcher.**
3. Dê **duplo-clique** em `instalar_traducao_windows.bat`.
4. Ele encontra o jogo sozinho e aplica. *(Se não achar, arraste a pasta do jogo — a que tem o `odin_sphere_leifthrasir.exe` — para a janela e pressione ENTER, ou arraste a pasta do jogo em cima do `.bat`.)*
5. Pronto! Abra o jogo pelo `odin_sphere_leifthrasir.exe` com o idioma em **English**.

### 🎮 Steam Deck / Linux

1. **Feche o jogo** e vá para o **Modo Desktop**.
2. Copie a pasta descompactada para o Deck (ex.: dentro da pasta do jogo, ou em `~/Downloads`).
3. Abra o **Konsole** nessa pasta e rode:
   ```bash
   chmod +x instalar_traducao_linux.sh
   ./instalar_traducao_linux.sh
   ```
   *(ou `./instalar_traducao_linux.sh "/caminho/da/pasta/do/jogo"`)*

> 💡 Se você já traduziu o jogo no PC e copiou a pasta do jogo inteira para o Deck, a tradução vai junto — não precisa instalar de novo.

O instalador **não duplica** os CPKs do jogo (2 GB o maior): ele anexa os textos traduzidos ao fim dos arquivos e repõe o índice, lendo tudo de volta para conferir. Se algo não bater, ele desfaz sozinho.

**Atualizando a tradução?** Rode o instalador da versão nova por cima: ele troca a anterior sem aumentar os arquivos.

---

## ↩️ Como reverter

Dê duplo-clique em `desinstalar_traducao_windows.bat` (ou rode `./desinstalar_traducao_linux.sh`). Os arquivos `Odin2_RE_UK.CPK`, `Odin2_BT_UK.CPK` e `Odin2_OR_UK.CPK` voltam **exatamente** ao que eram antes — o índice original fica guardado em `<nome do CPK>.ptbr.undo`, ao lado do jogo (não apague esses arquivos).

### 🎮 Botões de Xbox (opção *Controller prompts* do launcher)

O launcher também modifica os CPKs para trocar os ícones de botões.

- Os botões de Xbox **já estavam** ativos quando instalou a tradução? Pode jogar normalmente. Voltar para PlayStation remove a tradução — é só rodar o instalador de novo.
- Instalou a tradução **antes** de escolher os botões de Xbox? Pode trocar os botões à vontade, a tradução continua. Para desinstalar a tradução nesse caso, volte antes os botões para PlayStation no launcher (o desinstalador avisa).

Se você **reinstalar ou atualizar o jogo** pelo launcher, rode o instalador da tradução de novo.

---

## 🛠️ Como foi feito (resumo técnico)

1. Os textos ficam em três pacotes **CRI CPK**: `Odin2_RE_UK.CPK` (mensagens `msgsheet/*.fms` no formato **FMSB** da Vanillaware e os livros `ArchiveViewer/*.txt`), `Odin2_OR_UK.CPK` (Modo Clássico, strings separadas por byte nulo) e `Odin2_BT_UK.CPK` (as fontes).
2. Os textos foram extraídos, traduzidos e reempacotados mantendo **todos os códigos de controle** do jogo (`@f(n)`, `@t(n)`, `@X(n)`, ícones de botão `@#(n)`, `%d`/`%s`...).
3. As fontes (`HD_font_a/b/c.ftx`) são texturas **GNF/BC3** de PS4. As letras com til foram montadas a partir do til do ñ e do circunflexo do Ê de cada fonte, recodificadas em BC3 só nos blocos que mudam.
4. O instalador anexa os arquivos ao fim de cada CPK e reaponta as entradas do índice (TOC). Antes, ele confere se cada arquivo do jogo tem a mesma quantidade de textos que o traduzido, para não estragar uma versão diferente do jogo.

---

## ⚖️ Licença e uso

Esta é uma **tradução de fã**, feita **sem fins lucrativos** e **sem qualquer afiliação** com a Atlus, a Vanillaware ou a Sega.

- ✅ **Pode** baixar, usar e compartilhar **gratuitamente**.
- ✅ **Pode** repostar, desde que **credite** o autor e **mantenha** este aviso.
- ❌ **É proibido vender, cobrar, monetizar ou lucrar** de qualquer forma com esta tradução.
- ❌ **É proibido distribuir os arquivos do jogo.** Compartilhe **apenas o patch** deste repositório — nunca os `.CPK` ou outros arquivos originais.

*Odin Sphere* e todos os nomes relacionados são marcas registradas da **Atlus / Vanillaware / Sega**. Este projeto não é oficial e não substitui a compra do jogo. Veja [LICENSE.txt](LICENSE.txt).

---

## 🙏 Créditos

**Tradução e ferramentas:** **Wender_sky** *(Steam)*

Recomp para PC: [saulob/odin-sphere-leifthrasir-pc](https://github.com/saulob/odin-sphere-leifthrasir-pc).

Com a tradução instalada, o crédito aparece no sótão da Alice, acima de "Pegar o livro".
