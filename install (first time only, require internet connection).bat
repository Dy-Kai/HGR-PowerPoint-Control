call python -m venv venv
call venv\Scripts\activate
call cd "%~dp0\scripts\"
call pip install -r requirements.txt

pause