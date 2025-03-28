@echo off
setlocal ENABLEEXTENSIONS
echo Get macOS VMware Tools 3.0.4
echo ===============================
echo (c) Dave Parsons 2011-18

net session >NUL 2>&1
if %errorlevel% neq 0 (
    echo Administrator privileges required! 
    exit
)

pushd %~dp0

set KeyName="HKLM\SOFTWARE\Wow6432Node\VMware, Inc.\VMware Player"
:: delims is a TAB followed by a space
for /F "tokens=2* delims=	 " %%A in ('REG QUERY %KeyName% /v InstallPath') do set InstallPath=%%B
if "%InstallPath%" == "" (
    echo VMware is not installed
) else (
    echo VMware is installed at: "%InstallPath%"
)
for /F "tokens=2* delims=	 " %%A in ('REG QUERY %KeyName% /v ProductVersion') do set ProductVersion=%%B
echo VMware product version: %ProductVersion%

echo Getting VMware Tools...
gettools.exe
if NOT "%InstallPath%" == "" (
    xcopy /F /Y .\tools\darwin*.* "%InstallPath%"
)

popd

echo Finished!
