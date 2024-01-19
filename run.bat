@echo off

if exist .\venv\ (
    echo "Activating virtual environment..."
    CALL venv\Scripts\activate
) else (
    echo "Creating virtual environment..."
    python -m venv venv
    echo "Activating virtual environment..."
    CALL venv\Scripts\activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
)

echo "Starting application..."
flask run
