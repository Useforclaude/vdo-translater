@echo off
REM ===================================================
REM  Install Dependencies for Translation Pipeline
REM ===================================================

echo Installing required Python packages...
echo.

REM Core dependencies
pip install openai>=1.0.0
pip install python-dotenv
pip install pyyaml
pip install watchdog

REM Optional but recommended
pip install redis
pip install pydub
pip install ffmpeg-python
pip install rich
pip install click

REM For Whisper (if using local)
REM pip install openai-whisper

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo Now you can:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: python Test_Script_ep02.py
echo.
pause