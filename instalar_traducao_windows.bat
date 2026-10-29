@echo off
setlocal
chcp 65001 >nul
title Instalador Traducao PT-BR - Odin Sphere Leifthrasir
echo =====================================================================
echo       TRADUCAO PORTUGUES BRASILEIRO (PT-BR) - ODIN SPHERE LEIFTHRASIR
echo                   (Odin Sphere: Leifthrasir - Recomp PC)
echo =====================================================================
echo.

rem Detectar Python
set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERRO] Python 3 nao encontrado no sistema.
    echo Instale em https://www.python.org/downloads/ marcando "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

set "TARGET=%~1"
%PY% "%~dp0ferramentas\patcher.py" apply "%TARGET%" "%~dp0arquivos_traducao"
set "RESULT=%errorlevel%"

echo.
if "%RESULT%"=="0" (
    echo [SUCESSO] Traducao PT-BR instalada com sucesso!
    echo No launcher do jogo, mantenha o idioma em English, o padrao.
    echo Para remover a qualquer momento, use desinstalar_traducao_windows.bat.
) else (
    echo [ERRO] A instalacao nao pode ser concluida. Verifique a mensagem acima.
)
echo.
pause
exit /b %RESULT%
