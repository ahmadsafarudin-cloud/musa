@echo off
setlocal
echo Building SAFAR ANTI-BOTNET SECURITY for Windows...
py -m pip install --upgrade pip
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --windowed --name SAFAR_ANTI_BOTNET safar_antibotnet.py
if errorlevel 1 (
  echo Build failed. Check the error above.
  pause
  exit /b 1
)
echo.
echo SUCCESS. Your EXE is in the dist folder:
echo dist\SAFAR_ANTI_BOTNET.exe
pause
