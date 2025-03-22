@echo off
setlocal EnableDelayedExpansion

:SHOW_MAIN_MENU
    cls
    echo #####################################################
    echo #########          Servus %USERNAME%!         ###########
    echo #####################################################
    echo #########         PC-Name: %COMPUTERNAME%         ###########
    echo #####################################################
    echo #########        Last Edit: %LAST_EDIT_DATE%          #########
    echo #####################################################
    echo:
    echo =========================
    echo [1] Drucker hinzufuegen
    echo [2] PDF-Drucker hinzufuegen
    echo [3] Vertriebsordner verknuepfen
    echo [4] Scanordner verknuepfen
    echo [5] Desktoplinks erstellen(LHR,CT Online, BRZ Portal)
    echo [6] KKM Verknuepfung
    echo [7] M:,N: Laufwerke verbinden
    echo [8] Zusaetzlicher Zentrumsordner
    echo [0] Verlassen
    echo =========================
    echo:
    
    set "selection=0"
    set /p selection="Was moechtest du tun? (1-8)"
    
    if "%selection%"=="1" call :HANDLE_PRINTER_ADD
    if "%selection%"=="2" call :HANDLE_PDF_PRINTER
    if "%selection%"=="3" call :HANDLE_VERTRIEB
    if "%selection%"=="4" call :HANDLE_SCAN
    if "%selection%"=="5" call :HANDLE_DESKTOP_LINKS
    if "%selection%"=="6" call :HANDLE_KKM
    if "%selection%"=="7" call :HANDLE_NETWORK_DRIVES
    if "%selection%"=="8" call :HANDLE_ADDITIONAL_CENTER
    if "%selection%"=="0" exit /b
    
    goto SHOW_MAIN_MENU

:HANDLE_PRINTER_ADD
    call "%~dp0\printers.bat" ADD_PRINTER "%zentrum%"
    goto SHOW_MAIN_MENU

:HANDLE_PDF_PRINTER
    call "%~dp0\printers.bat" ADD_PDF_PRINTER
    goto SHOW_MAIN_MENU

:HANDLE_VERTRIEB
    call "%~dp0\network.bat" MAP_VERTRIEB
    goto SHOW_MAIN_MENU

:HANDLE_SCAN
    call "%~dp0\network.bat" MAP_SCAN "%scanfolder%"
    goto SHOW_MAIN_MENU

:HANDLE_DESKTOP_LINKS
    call "%~dp0\shortcuts.bat" CREATE_ALL_SHORTCUTS
    goto SHOW_MAIN_MENU

:HANDLE_KKM
    call "%~dp0\shortcuts.bat" CREATE_KKM_RDP "%kkm%" "%DEFAULT_DESKTOP_PATH%"
    goto SHOW_MAIN_MENU

:HANDLE_NETWORK_DRIVES
    if "%zentrum%"=="3000" (
        call "%~dp0\network.bat" MAP_TEESDORF_DRIVES
    ) else (
        call "%~dp0\network.bat" MAP_PROVINCE_DRIVES "%zentrum%"
    )
    goto SHOW_MAIN_MENU

:HANDLE_ADDITIONAL_CENTER
    call "%~dp0\network.bat" MAP_ADDITIONAL_CENTER
    goto SHOW_MAIN_MENU 