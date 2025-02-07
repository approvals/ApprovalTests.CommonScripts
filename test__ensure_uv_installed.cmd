setlocal

@REM should not have uv installed yet
where /q uv
if not ERRORLEVEL 1 (
  echo delete ^%USERPROFILE^%\.local before running this test
  exit /b 1
)

@REM call ensure_uv_installed and check if it downloads uv
call ensure_uv_installed.cmd 2>&1 | findstr /b /c:"Downloading uv"
if ERRORLEVEL 1 exit /b 1

set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where /q uv || exit /b 1

@REM should not install uv again
call ensure_uv_installed.cmd 2>&1 | findstr /b /c:"Downloading uv"
if not ERRORLEVEL 1 exit /b 1
