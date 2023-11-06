
:: ======================================================
:: RUN THIS SCRIPT TO EXPORT YOUR APPLICATION INTO AN EXE
:: ======================================================

:: CHANGE THIS PATH FOR YOUR OWN PC
set PYTHON_VENV_PATH="C:\Users\oguzh\myVenv\Lib\site-packages"

:: DON'T TOUCH BELOW
set MAIN_PATH=".\src\main_window.py"

pyinstaller %MAIN_PATH% --onefile --noconsole --paths %PYTHON_VENV_PATH%

rmdir /s /q ".\build"
move ".\dist\main_window.exe" ".\main_window.exe"
rmdir /s /q ".\dist"
