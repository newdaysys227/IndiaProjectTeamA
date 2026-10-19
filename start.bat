@echo off
cd /d "%~dp0"

echo ============================================
echo  Web Security Academy (Learning) - setup
echo ============================================
echo.

echo [1/4] Installing the libraries...
python -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo [2/4] Making the database...
python manage.py migrate
if errorlevel 1 goto error

echo.
echo [3/4] Adding demo data...
python manage.py seed
if errorlevel 1 goto error

echo.
echo [4/4] Starting the server. Open this URL in your browser:
echo.
echo        http://127.0.0.1:8000/
echo.
echo   (To stop: press Ctrl + C in this window)
echo.
start "" http://127.0.0.1:8000/
python manage.py runserver 127.0.0.1:8000
goto end

:error
echo.
echo *** Something went wrong ***
echo Please check that Python is installed ( python --version ).
echo You can get Python at https://www.python.org/
pause

:end
