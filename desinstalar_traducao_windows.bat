@echo off
setlocal
chcp 65001 >nul
title Desinstalador Traducao PT-BR - Odin Sphere Leifthrasir
echo =====================================================================
echo       DESINSTALAR TRADUCAO PT-BR - ODIN SPHERE LEIFTHRASIR
echo                   (Restaura o jogo original em ingles)
echo =====================================================================
echo.

set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERRO] Python 3 nao encontrado no sistema.
    pause
    exit /b 1
)

set "TARGET=%~1"
%PY% "%~dp0ferramentas\patcher.py" revert "%TARGET%"
set "RESULT=%errorlevel%"

echo.
pause
exit /b %RESULT%
