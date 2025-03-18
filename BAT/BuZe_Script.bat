@echo off &title "Willkommen bei der OEAMTC Fahrtechnik :-)"
echo #####################################################
echo #########          Servus %USERNAME%!         ###########
echo #####################################################
echo #########         PC-Name: %COMPUTERNAME%         ###########
echo #####################################################


:: Zentrum wird durch Kuerzel ausgewaehlt 
echo:
echo =========================
echo Welches Zentrum?
echo:
set /p zentrumskuerzel= "[SFD,MLK,OOE,TRL,LEB,KAL,KTN,TDF] :"
goto ZENTRUMSAUSWAHL
goto MAINMENU



pause
EXIT 

:: ------------------------------------------------------------------------------------------------------------
:: ScriptSchnipsel

:MAINMENU
    cls
    echo #####################################################
    echo #########          Servus %USERNAME%!         ###########
    echo #####################################################
    echo #########         PC-Name: %COMPUTERNAME%         ###########
    echo #####################################################
    echo #####################################################
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
    set selection=0
    set /p selection="Was moechtest du tun? (1-7)"

    if /I %selection% EQU 1 (
        goto DRUCKER_VERBINDEN
    ) 
    if /I %selection% EQU 2 (
        goto PDF_DRUCKER
    )
    if /I %selection% EQU 3 (
        goto VERTRIEB_EINRICHTEN
    )
    if /I %selection% EQU 4 (
        goto SCAN_EINRICHTEN
    )
    if /I %selection% EQU 5 (
        goto DESKTOP_LINKS
    )
    if /I %selection% EQU 6 (
        goto KKMLINK
    )
    if /I %selection% EQU 7 (
        if /I %zentrum% EQU 3000 (
            goto SHARES_TEESDORF
        ) else (
            goto SHARES_PROVINZ
        )
    )
        if /I %selection% EQU 8 (
        goto ZUSAETZLICHES_ZENTRUM_SHARE
    ) 

    if /I %selection% EQU 0 (
        goto ENDE
    )
    goto MAINMENU

:ZENTRUMSAUSWAHL
    ::Umwandlung Zentrumskürzel

    if /I "%zentrumskuerzel%" EQU "SFD" (
        set zentrum=3110
        set kkm=n3110
        set scanfolder="\\atlas\ftgroups\3110\Scan Dateien"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "MLK" (
        set zentrum=3130
        set kkm=n3130
        set scanfolder="nicht_vorhanden"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "OOE" (
        set zentrum=3140
        set kkm=n3140
        set scanfolder="\\atlas\ftgroups\3140\SCAN-Dateien"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "TRL" (
        set zentrum=3160
        set kkm=n3160
        set scanfolder="\\atlas\ftgroups\3160\SCAN-Dateien"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "LEB" (
        set zentrum=3180
        set kkm=n3180
        set scanfolder="\\atlas\ftgroups\3180\SCAN-Dateien"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "KAL" (
        set zentrum=3280
        set kkm=n3280
        set scanfolder="nicht_vorhanden"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "KTN" (
        set zentrum=3190
        set kkm=n3190
        set scanfolder="\\atlas\ftgroups\3190\Scan"
        goto MAINMENU
    )
    if /I "%zentrumskuerzel%" EQU "TDF" (
        set zentrum=3000
        set kkm=n3100
        set scanfolder="\\n3000\tt\Scan-Dateien"
        goto MAINMENU
    )
:PRINTERS
    :: Frage ob ein Drucker verbunden werden soll
    set /p cc="Moechtest du einen weiteren Drucker verbinden?: [J/N]"
    if /I "%cc%" EQU "J" goto DRUCKER_VERBINDEN
    if /I "%cc%" EQU "N" goto MAINMENU
    goto PRINTERS

:DRUCKER_VERBINDEN
    :: Welcher Drucker soll verbunden werden?
    set /p printers="Druckername?:"
    set "servers=n%zentrum%"

    for %%s in (%servers%) do (
    for %%p in (%printers%) do (
        :: Install printer if it doesn't exist
        RUNDLL32 printui.dll,PrintUIEntry /in /n "\\%%s\%%p"
        echo Printer "\\%%s\%%p" installed.  
    )
    )
    goto PRINTERS

:PDF_DRUCKER
    :: Set up PDF printers
    set "printers=pdf-mail pdf-mail-ft"
    set "servers=pdfpr01"

    for %%s in (%servers%) do (
    for %%p in (%printers%) do (
        :: Install printer
        RUNDLL32 printui.dll,PrintUIEntry /in /n "\\%%s\%%p"
        echo Printer "\\%%s\%%p" installed.
    )
    )
    goto MAINMENU

:VERTRIEB_EINRICHTEN 
    set /p vertrieb_buchstabe="Welcher Laufwerksbuchstabe fuer den Vertriebsordner?:"
    net use %vertrieb_buchstabe%: /delete
    net use %vertrieb_buchstabe%: "\\n3000\tt\VERTRIEB  NFZ chg"
    echo "Vertriebsordner als Laufwerk %vertrieb_buchstabe% eingerichtet."
    goto MAINMENU

:SCAN_EINRICHTEN
    if /I "%scanfolder%" EQU "nicht_vorhanden" (
        echo "Fuer dieses Zentrum gibt es keinen Scanordner"
        goto MAINMENU
    )
    set /p scan_buchstabe="Welcher Laufwerksbuchstabe fuer den ScanOrdner?:"
    net use %scan_buchstabe%: /delete
    net use %scan_buchstabe%: %scanfolder%
    echo "Der Scanordner wurde als Laufwerk %scan_buchstabe% eingerichtet."
    echo %scanfolder%
    pause
    goto MAINMENU

:DESKTOP_LINKS

    ::Outlook_Link
    set SavePath="%HOMEPATH%\Desktop"
    set SourcePath="C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    copy %SourcePath%\outlook.lnk %SavePath%
    echo "Outlook link wurde erstellt"

    ::Mein_Cockpit_Link
    set SavePath="%HOMEPATH%\Desktop"
    set URL="https://lhrportal.oeamtc.at/Self/login"
    set FileName="%SavePath%\MeinCockpit.url"

    (
        echo [InternetShortcut]
        echo URL=%URL%
    ) > "%FileName%"

    echo "Mein Cockpit Link erstellt"

    :: CT Online Link
    set SavePath="%HOMEPATH%\Desktop"
    set URL="https://www.ctonline.at/auth"
    set FileName="%SavePath%\CTOnline.url"

    (
        echo [InternetShortcut]
        echo URL=%URL%
    ) > "%FileName%"
    echo "CT Online Link erstellt"

    :: BRZ Austria Portal Link
    set SavePath="%HOMEPATH%\Desktop"
    set URL="https://secure.portal.at/pat/#FSR"
    set FileName="%SavePath%\BRZ_PortalAustria.url"

    (
        echo [InternetShortcut]
        echo URL=%URL%
    ) > "%FileName%"

    echo "BRZ PortalAustria Link erstellt"
    goto MAINMENU
:SHARES_PROVINZ

    :: Delete existing network drives
    net use M: /delete
    net use N: /delete

    :: Map network drives
    net use M: \\atlas\ftusers\%USERNAME%
    net use N: \\atlas\ftgroups\%zentrum%

    echo "Die Laufwerke M: und N: wurden eingerichtet."
    goto MAINMENU
:SHARES_TEESDORF

    :: Delete existing network drives
    net use M: /delete
    net use N: /delete

    :: Map network drives
    net use M: \\n3000\users\%USERNAME%
    net use N: \\n3000\tt

    echo "Die Laufwerke M: und N: wurden eingerichtet."
    goto MAINMENU

:ZUSAETZLICHES_ZENTRUM_SHARE

    echo "Welcher Zentrumsordner soll hinzugefuegt werden?"
    echo "[SFD,MLK,OOE,TRL,LEB,KAL,KTN,TDF]"
    set /p zus_zentrumskuerzel = ":"

::Umwandlung Zusätzliches Zentrumskürzel

    if /I "%zus_zentrumskuerzel%" EQU "SFD" (
        set zus_zentrum=3110
    )
    if /I "%zus_zentrumskuerzel%" EQU "MLK" (
        set zus_zentrum=3130
    )
    if /I "%zus_zentrumskuerzel%" EQU "OOE" (
        set zus_zentrum=3140
    )
    if /I "%zus_zentrumskuerzel%" EQU "TRL" (
        set zus_zentrum=3160
    )
    if /I "%zus_zentrumskuerzel%" EQU "LEB" (
        set zus_zentrum=3180
    )
    if /I "%zus_zentrumskuerzel%" EQU "KAL" (
        set zus_zentrum=3280
    )
    if /I "%zus_zentrumskuerzel%" EQU "KTN" (
        set zus_zentrum=3190
    )
    if /I "%zus_zentrumskuerzel%" EQU "TDF" (
        set zus_zentrum=3000
    )
    
    echo %zus_zentrum%
    set /p zus_zentrum_buchstabe="Welcher Laufwerksbuchstabe fuer den Zentrumsordner?:"

        if /I %zus_zentrum% EQU 3000 (
            net use %zus_zentrum_buchstabe%: /delete
            net use %zus_zentrum_buchstabe%: "\\n3000\tt"
            echo "Zentrumsordner wurde als Laufwerk %zentrum_buchstabe% eingerichtet."
        ) else (
            net use %zus_zentrum_buchstabe%: /delete
            net use %zus_zentrum_buchstabe%: "\\atlas\ftgroups\%zus_zentrum%"
            echo "Zentrumsordner wurde als Laufwerk %zentrum_buchstabe% eingerichtet."
        )
        echo %zus_zentrum_buchstabe%
        pause
    goto MAINMENU


:KKMLINK
    :: KKM RDP Verknüpfung für Desktop erstellen

    :: Set the path and file name 
    set "FileName=%homepath%\Desktop\KKM.rdp"

    :: Create the .rdp file
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
    ) > "%FileName%"

    echo "KKM Verknuepfung erstellt"
    goto MAINMENU

:ENDE