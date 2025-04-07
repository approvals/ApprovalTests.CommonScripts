@echo off

call python --version
call python -m pip install --upgrade pip --requirement requirements.dev.txt
call python -m pytest . -v
