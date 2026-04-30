@echo off
echo ========================================
echo  Instalador - Engaja Tube (Valoriza)
echo ========================================
echo.
echo Instalando dependencias necessarias...
echo.

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo  Instalacao concluida!
echo ========================================
echo.
echo Para executar o programa, digite:
echo python view.py
echo.
pause
