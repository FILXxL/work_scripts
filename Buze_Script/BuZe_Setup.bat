@echo off
setlocal EnableDelayedExpansion
title "Willkommen bei der OEAMTC Fahrtechnik :-)"

:: Global Configuration
set "LAST_EDIT_DATE=220324"
set "VERSION=2.0"
set "ATLAS_PATH=\\atlas"
set "TEESDORF_PATH=\\n3000"
set "DEFAULT_DESKTOP_PATH=%HOMEPATH%\Desktop"
set "DEFAULT_OUTLOOK_PATH=C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
set "MEIN_COCKPIT_URL=https://lhrportal.oeamtc.at/Self/login"
set "CT_ONLINE_URL=https://www.ctonline.at/auth"
set "BRZ_PORTAL_URL=https://secure.portal.at/pat/#FSR"

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

goto SHOW_MAIN_MENU

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
    
    if "%selection%"=="1" goto ADD_PRINTER
    if "%selection%"=="2" goto ADD_PDF_PRINTER
    if "%selection%"=="3" goto MAP_VERTRIEB
    if "%selection%"=="4" goto MAP_SCAN
    if "%selection%"=="5" goto CREATE_ALL_SHORTCUTS
    if "%selection%"=="6" goto CREATE_KKM_RDP
    if "%selection%"=="7" (
        if "%zentrum%"=="3000" (
            goto MAP_TEESDORF_DRIVES
        ) else (
            goto MAP_PROVINCE_DRIVES
        )
    )
    if "%selection%"=="8" goto MAP_ADDITIONAL_CENTER
    if "%selection%"=="0" exit /b
    
    goto SHOW_MAIN_MENU

:ADD_PRINTER
    set /p printers="Druckername?:"
    set "servers=n%zentrum%"
    
    for %%s in (%servers%) do (
        for %%p in (%printers%) do (
            RUNDLL32 printui.dll,PrintUIEntry /in /n "\\%%s\%%p"
            echo Printer "\\%%s\%%p" installed.
        )
    )
    
    set /p cc="Moechtest du einen weiteren Drucker verbinden?: [J/N]"
    if /I "%cc%"=="J" goto ADD_PRINTER
    goto SHOW_MAIN_MENU

:ADD_PDF_PRINTER
    set "printers=pdf-mail pdf-mail-ft"
    set "servers=pdfpr01"
    
    for %%s in (%servers%) do (
        for %%p in (%printers%) do (
            RUNDLL32 printui.dll,PrintUIEntry /in /n "\\%%s\%%p"
            echo Printer "\\%%s\%%p" installed.
        )
    )
    goto SHOW_MAIN_MENU

:MAP_VERTRIEB
    set /p vertrieb_buchstabe="Welcher Laufwerksbuchstabe fuer den Vertriebsordner?:"
    net use %vertrieb_buchstabe%: /delete
    net use %vertrieb_buchstabe%: "%TEESDORF_PATH%\tt\VERTRIEB  NFZ chg"
    echo "Vertriebsordner als Laufwerk %vertrieb_buchstabe% eingerichtet."
    goto SHOW_MAIN_MENU

:MAP_SCAN
    if "%scanfolder%"=="nicht_vorhanden" (
        echo "Fuer dieses Zentrum gibt es keinen Scanordner"
        goto SHOW_MAIN_MENU
    )
    set /p scan_buchstabe="Welcher Laufwerksbuchstabe fuer den ScanOrdner?:"
    net use %scan_buchstabe%: /delete
    net use %scan_buchstabe%: "%scanfolder%"
    echo "Der Scanordner wurde als Laufwerk %scan_buchstabe% eingerichtet."
    goto SHOW_MAIN_MENU

:CREATE_ALL_SHORTCUTS
    :: Outlook shortcut
    if exist "%DEFAULT_OUTLOOK_PATH%\outlook.lnk" (
        copy "%DEFAULT_OUTLOOK_PATH%\outlook.lnk" "%DEFAULT_DESKTOP_PATH%"
        echo "Outlook link wurde erstellt"
    ) else (
        echo "Outlook shortcut konnte nicht gefunden werden"
    )
    
    :: Mein Cockpit shortcut
    (
        echo [InternetShortcut]
        echo URL=%MEIN_COCKPIT_URL%
    ) > "%DEFAULT_DESKTOP_PATH%\MeinCockpit.url"
    echo "Mein Cockpit Link erstellt"
    
    :: CT Online shortcut
    (
        echo [InternetShortcut]
        echo URL=%CT_ONLINE_URL%
    ) > "%DEFAULT_DESKTOP_PATH%\CTOnline.url"
    echo "CT Online Link erstellt"
    
    :: BRZ Portal shortcut
    (
        echo [InternetShortcut]
        echo URL=%BRZ_PORTAL_URL%
    ) > "%DEFAULT_DESKTOP_PATH%\BRZ_PortalAustria.url"
    echo "BRZ PortalAustria Link erstellt"
    goto SHOW_MAIN_MENU

:CREATE_KKM_RDP
    :: Create KKM RDP file
    (
        echo screen mode id:i:2
        echo use multimon:i:0
        echo desktopwidth:i:1920
        echo desktopheight:i:1080
        echo session bpp:i:24
        echo winposstr:s:0,1,922,-1080,2873,0
        echo compression:i:1
        echo keyboardhook:i:2
        echo audiocapturemode:i:0
        echo videoplaybackmode:i:1
        echo connection type:i:7
        echo networkautodetect:i:1
        echo bandwidthautodetect:i:1
        echo displayconnectionbar:i:1
        echo enableworkspacereconnect:i:0
        echo disable wallpaper:i:0
        echo allow font smoothing:i:0
        echo allow desktop composition:i:0
        echo disable full window drag:i:1
        echo disable menu anims:i:1
        echo disable themes:i:0
        echo disable cursor setting:i:0
        echo bitmapcachepersistenable:i:1
        echo full address:s:%kkm%
        echo audiomode:i:0
        echo redirectprinters:i:1
        echo redirectcomports:i:0
        echo redirectsmartcards:i:1
        echo redirectwebauthn:i:1
        echo redirectclipboard:i:1
        echo redirectposdevices:i:0
        echo autoreconnection enabled:i:1
        echo authentication level:i:2
        echo prompt for credentials:i:0
        echo negotiate security layer:i:1
        echo remoteapplicationmode:i:0
        echo alternate shell:s:
        echo shell working directory:s:
        echo gatewayhostname:s:
        echo gatewayusagemethod:i:4
        echo gatewaycredentialssource:i:4
        echo gatewayprofileusagemethod:i:0
        echo promptcredentialonce:i:0
        echo gatewaybrokeringtype:i:0
        echo use redirection server name:i:0
        echo rdgiskdcproxy:i:0
        echo kdcproxyname:s:
        echo enablerdsaadauth:i:0
        echo drivestoredirect:s:
    ) > "%DEFAULT_DESKTOP_PATH%\KKM.rdp"
    
    echo "KKM Verknuepfung erstellt"
    goto SHOW_MAIN_MENU

:MAP_TEESDORF_DRIVES
    net use M: /delete
    net use N: /delete
    net use M: "%TEESDORF_PATH%\users\%USERNAME%"
    net use N: "%TEESDORF_PATH%\tt"
    echo "Die Laufwerke M: und N: wurden eingerichtet."
    goto SHOW_MAIN_MENU

:MAP_PROVINCE_DRIVES
    net use M: /delete
    net use N: /delete
    net use M: "%ATLAS_PATH%\ftusers\%USERNAME%"
    net use N: "%ATLAS_PATH%\ftgroups\%zentrum%"
    echo "Die Laufwerke M: und N: wurden eingerichtet."
    goto SHOW_MAIN_MENU

:MAP_ADDITIONAL_CENTER
    echo "Welcher Zentrumsordner soll hinzugefuegt werden?"
    echo "[SFD,MLK,OOE,TRL,LEB,KAL,KTN,TDF]"
    set /p zus_zentrumskuerzel=
    
    if /I "%zus_zentrumskuerzel%"=="SFD" set "zus_zentrum=3110"
    if /I "%zus_zentrumskuerzel%"=="MLK" set "zus_zentrum=3130"
    if /I "%zus_zentrumskuerzel%"=="OOE" set "zus_zentrum=3140"
    if /I "%zus_zentrumskuerzel%"=="TRL" set "zus_zentrum=3160"
    if /I "%zus_zentrumskuerzel%"=="LEB" set "zus_zentrum=3180"
    if /I "%zus_zentrumskuerzel%"=="KAL" set "zus_zentrum=3280"
    if /I "%zus_zentrumskuerzel%"=="KTN" set "zus_zentrum=3190"
    if /I "%zus_zentrumskuerzel%"=="TDF" set "zus_zentrum=3000"
    
    set /p zus_zentrum_buchstabe="Welcher Laufwerksbuchstabe fuer den Zentrumsordner?:"
    
    if "%zus_zentrum%"=="3000" (
        net use %zus_zentrum_buchstabe%: /delete
        net use %zus_zentrum_buchstabe%: "%TEESDORF_PATH%\tt"
    ) else (
        net use %zus_zentrum_buchstabe%: /delete
        net use %zus_zentrum_buchstabe%: "%ATLAS_PATH%\ftgroups\%zus_zentrum%"
    )
    echo "Zentrumsordner wurde als Laufwerk %zus_zentrum_buchstabe% eingerichtet."
    goto SHOW_MAIN_MENU 