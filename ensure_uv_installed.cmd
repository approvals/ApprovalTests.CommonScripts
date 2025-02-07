@echo off
setlocal

@REM Clear PsModulePath to avoid conflicts with PWSH, which happens in GitHub actions
set "PsModulePath="
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" || goto :ERROR
