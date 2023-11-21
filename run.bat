@echo off

if exist .\venv\ (
    echo "Venv found"
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    pip install -r requirements.txt
)

CALL venv\Scripts\activate
echo Starting application...
flask run
