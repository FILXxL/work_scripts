@echo off

if "%~1"=="ADD_PRINTER" goto ADD_PRINTER
if "%~1"=="ADD_PDF_PRINTER" goto ADD_PDF_PRINTER
exit /b

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
    exit /b

:ADD_PDF_PRINTER
    set "printers=pdf-mail pdf-mail-ft"
    set "servers=pdfpr01"
    
    for %%s in (%servers%) do (
        for %%p in (%printers%) do (
            RUNDLL32 printui.dll,PrintUIEntry /in /n "\\%%s\%%p"
            echo Printer "\\%%s\%%p" installed.
        )
    )
    exit /b 