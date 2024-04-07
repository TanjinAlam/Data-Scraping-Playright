@echo off

echo Installing Python dependencies...
pip install -r requirements.txt

playwright install chromium

echo Setup completed.
