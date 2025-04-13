@echo off

call python --version
python -m venv .venv
call .venv\Scripts\activate.bat

call python -m pip install --upgrade pip --requirement requirements.dev.txt
call python -m pytest . -v && python -m mypy .
