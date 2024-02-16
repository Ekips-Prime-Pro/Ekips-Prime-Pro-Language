REM TODO: Update the FTP server details and the local folder path and check if it works
@echo off

REM FTP server details
set FTP_SERVER=parameros.net
set FTP_USERNAME=username
set FTP_PASSWORD=password

REM Local folder paths
set LOCAL_FOLDER=%~dp0
set TEMP_FOLDER=%LOCAL_FOLDER%temp

REM Check for version file
set VERSION_FILE=%LOCAL_FOLDER%version.txt
if exist "%VERSION_FILE%" (
    set /p CURRENT_VERSION=<"%VERSION_FILE%"
) else (
    set CURRENT_VERSION=0
)

REM Download the latest version 
echo Downloading latest version...
ftp -n -i -s:"%LOCAL_FOLDER%ftp_commands.txt" %FTP_SERVER%

REM Check if there is a new update
set /p LATEST_VERSION=<"%TEMP_FOLDER%version.txt"
if %LATEST_VERSION% gtr %CURRENT_VERSION% (
    echo New update available. Updating...

    REM Delete old content
    echo Deleting old content...
    rmdir /s /q "%LOCAL_FOLDER%Compiler"
    rmdir /s /q "%LOCAL_FOLDER%GUI"

    REM Unpack new content
    echo Unpacking new content...
    powershell -command "Expand-Archive -Path '%TEMP_FOLDER%\update.zip' -DestinationPath '%LOCAL_FOLDER%'"

    REM Update version file
    echo %LATEST_VERSION% > "%VERSION_FILE%"

    echo Update completed successfully.
) else (
    echo No new update available.
)

REM Clean up temporary files
echo Cleaning up...
rmdir /s /q "%TEMP_FOLDER%"

pause
@echo off

REM Set the FTP server details
set FTP_SERVER=parameros.net
set FTP_USERNAME=username
set FTP_PASSWORD=password

REM Set the local folder path
set LOCAL_FOLDER=%~dp0

REM Set the remote file path
set REMOTE_FILE=/path/to/update.zip

REM Delete the old content
del /q %LOCAL_FOLDER%*

REM Download the update file
echo Downloading update...
echo user %FTP_USERNAME% %FTP_PASSWORD%> ftp.txt
echo binary>> ftp.txt
echo get %REMOTE_FILE%>> ftp.txt
echo quit>> ftp.txt
ftp -s:ftp.txt %FTP_SERVER%
del /q ftp.txt

REM Unpack the update file
echo Unpacking update...
powershell -command "Expand-Archive -Path '%LOCAL_FOLDER%update.zip' -DestinationPath '%LOCAL_FOLDER%' -Force"
del /q %LOCAL_FOLDER%update.zip

echo Update completed successfully.
pause
@echo off
echo Updating Code...
ftp -i -s:ftp_commands.txt parameros.net
echo Update complete.
