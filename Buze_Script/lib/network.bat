@echo off

if "%~1"=="MAP_VERTRIEB" goto MAP_VERTRIEB
if "%~1"=="MAP_SCAN" goto MAP_SCAN
if "%~1"=="MAP_TEESDORF_DRIVES" goto MAP_TEESDORF_DRIVES
if "%~1"=="MAP_PROVINCE_DRIVES" goto MAP_PROVINCE_DRIVES
if "%~1"=="MAP_ADDITIONAL_CENTER" goto MAP_ADDITIONAL_CENTER
exit /b

:MAP_VERTRIEB
    set /p vertrieb_buchstabe="Welcher Laufwerksbuchstabe fuer den Vertriebsordner?:"
    net use %vertrieb_buchstabe%: /delete
    net use %vertrieb_buchstabe%: "%TEESDORF_PATH%\tt\VERTRIEB  NFZ chg"
    echo "Vertriebsordner als Laufwerk %vertrieb_buchstabe% eingerichtet."
    exit /b

:MAP_SCAN
    if "%scanfolder%"=="nicht_vorhanden" (
        echo "Fuer dieses Zentrum gibt es keinen Scanordner"
        exit /b
    )
    set /p scan_buchstabe="Welcher Laufwerksbuchstabe fuer den ScanOrdner?:"
    net use %scan_buchstabe%: /delete
    net use %scan_buchstabe%: "%scanfolder%"
    echo "Der Scanordner wurde als Laufwerk %scan_buchstabe% eingerichtet."
    exit /b

:MAP_TEESDORF_DRIVES
    net use M: /delete
    net use N: /delete
    net use M: "%TEESDORF_PATH%\users\%USERNAME%"
    net use N: "%TEESDORF_PATH%\tt"
    echo "Die Laufwerke M: und N: wurden eingerichtet."
    exit /b

:MAP_PROVINCE_DRIVES
    net use M: /delete
    net use N: /delete
    net use M: "%ATLAS_PATH%\ftusers\%USERNAME%"
    net use N: "%ATLAS_PATH%\ftgroups\%zentrum%"
    echo "Die Laufwerke M: und N: wurden eingerichtet."
    exit /b

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
    exit /b 