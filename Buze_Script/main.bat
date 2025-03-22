@echo off
setlocal EnableDelayedExpansion
title "Willkommen bei der OEAMTC Fahrtechnik :-)"

:: Import configuration
call "%~dp0\config\config.bat"

:: Display welcome message
cls
echo #####################################################
echo #########          Servus %USERNAME%!         ###########
echo #####################################################
echo #########         PC-Name: %COMPUTERNAME%         ###########
echo #####################################################
echo #########        Last Edit: %LAST_EDIT_DATE%          #########
echo #####################################################

:: Get center selection
echo:
echo =========================
echo Welches Zentrum?
echo [SFD,MLK,OOE,TRL,LEB,KAL,KTN,TDF]:
set /p zentrumskuerzel=

:: Set center configuration
if /I "%zentrumskuerzel%" EQU "SFD" (
    set "zentrum=3110"
    set "kkm=n3110"
    set "scanfolder=\\atlas\ftgroups\3110\Scan Dateien"
) else if /I "%zentrumskuerzel%" EQU "MLK" (
    set "zentrum=3130"
    set "kkm=n3130"
    set "scanfolder=nicht_vorhanden"
) else if /I "%zentrumskuerzel%" EQU "OOE" (
    set "zentrum=3140"
    set "kkm=n3140"
    set "scanfolder=\\atlas\ftgroups\3140\SCAN-Dateien"
) else if /I "%zentrumskuerzel%" EQU "TRL" (
    set "zentrum=3160"
    set "kkm=n3160"
    set "scanfolder=\\atlas\ftgroups\3160\SCAN-Dateien"
) else if /I "%zentrumskuerzel%" EQU "LEB" (
    set "zentrum=3180"
    set "kkm=n3180"
    set "scanfolder=\\atlas\ftgroups\3180\SCAN-Dateien"
) else if /I "%zentrumskuerzel%" EQU "KAL" (
    set "zentrum=3280"
    set "kkm=n3280"
    set "scanfolder=nicht_vorhanden"
) else if /I "%zentrumskuerzel%" EQU "KTN" (
    set "zentrum=3190"
    set "kkm=n3190"
    set "scanfolder=\\atlas\ftgroups\3190\Scan"
) else if /I "%zentrumskuerzel%" EQU "TDF" (
    set "zentrum=3000"
    set "kkm=n3100"
    set "scanfolder=\\n3000\tt\Scan-Dateien"
)

:: Export variables for child scripts
endlocal & (
    set "zentrum=%zentrum%"
    set "kkm=%kkm%"
    set "scanfolder=%scanfolder%"
    set "LAST_EDIT_DATE=%LAST_EDIT_DATE%"
    set "DEFAULT_DESKTOP_PATH=%HOMEPATH%\Desktop"
    set "DEFAULT_OUTLOOK_PATH=C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    set "MEIN_COCKPIT_URL=%MEIN_COCKPIT_URL%"
    set "CT_ONLINE_URL=%CT_ONLINE_URL%"
    set "BRZ_PORTAL_URL=%BRZ_PORTAL_URL%"
    set "ATLAS_PATH=%ATLAS_PATH%"
    set "TEESDORF_PATH=%TEESDORF_PATH%"
)

:: Import function libraries after center selection
call "%~dp0\lib\menu.bat"
call "%~dp0\lib\printers.bat"
call "%~dp0\lib\network.bat"
call "%~dp0\lib\shortcuts.bat"

:: Show main menu
call :SHOW_MAIN_MENU

exit /b 