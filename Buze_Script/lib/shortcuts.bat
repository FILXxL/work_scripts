@echo off

if "%~1"=="CREATE_ALL_SHORTCUTS" goto CREATE_ALL_SHORTCUTS
if "%~1"=="CREATE_KKM_RDP" goto CREATE_KKM_RDP
exit /b

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
    exit /b

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
        echo full address:s:%~2
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
    ) > "%~3\KKM.rdp"
    
    echo "KKM Verknuepfung erstellt"
    exit /b 