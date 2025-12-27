@echo off
echo ========================================
echo Building Monika.exe
echo ========================================
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Building executable...

REM Build with PyInstaller
REM --onefile: Single exe file
REM --noconsole: No console window (remove this for debugging)
REM --icon: Custom icon (if you have monika.ico)
REM --add-data: Include image files

python -m PyInstaller --onefile --noconsole --name "Monika" --icon "monika.ico" --add-data "monika.png;." --add-data "jumpscare.png;." --add-data "jumpscare1.png;." --add-data "jumpscare2.png;." --add-data "jumpscare.wav;." --add-data "error.wav;." --add-data "ambient.wav;." --add-data "laugh.wav;." --add-data "glitch.wav;." monika.py

echo.
echo ========================================
echo Build complete!
echo Your exe is in the 'dist' folder
echo ========================================
echo.
echo Don't forget to put these files in the same folder as monika.py before building:
echo - monika.png (transparent Monika for overlay)
echo - jumpscare.png (main jumpscare image)
echo - jumpscare1.png, jumpscare2.png (optional extra jumpscares)
echo.
pause
