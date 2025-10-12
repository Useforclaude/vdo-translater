@echo off
REM ===================================================
REM  Run Thai-English Translation Pipeline
REM ===================================================

REM Set your OpenAI API Key here (use .env file or set manually)
REM set OPENAI_API_KEY=sk-YOUR-KEY-HERE
REM Or load from .env file: python -c "from dotenv import load_dotenv; load_dotenv()"
set OPENAI_API_KEY=%OPENAI_API_KEY%

REM Optional settings
set CONFIG_MODE=cost_optimized
set CACHE_DIR=.cache
set LOG_LEVEL=INFO
set MAX_WORKERS=4

REM Display configuration
echo ====================================
echo Thai-English Translation Pipeline
echo ====================================
echo Mode: %CONFIG_MODE%
echo Cache: %CACHE_DIR%
echo Workers: %MAX_WORKERS%
echo ====================================
echo.

REM Run the test script
python Test_Script_ep02.py

REM Pause to see results
pause