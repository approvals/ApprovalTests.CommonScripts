@echo off
set "SOURCE_FILE=%~n0.txt"
for /f "delims=" %%i in (%SOURCE_FILE%) do (
    cmd /c %%i
)
