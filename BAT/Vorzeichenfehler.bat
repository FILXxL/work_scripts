@echo off
setlocal enabledelayedexpansion

:: Set the keyword to find and toggle comment
set "keyword=log=C:\Temp\oracle.log"

:: Set the input and output file paths
set "inputFile=C:\Orbis\sql.ini"
set "outputFile=sql_temp.ini"

:: Ensure the output file is empty before starting
echo. > "%outputFile%"

:: Read the input file line by line
for /f "tokens=*" %%A in ('type "%inputFile%"') do (
    set "line=%%A"
    set "trimmedLine=!line:;=!"
    set "trimmedLine=!trimmedLine:~0,1!!trimmedLine:~1!"

    :: Check if the line (trimmed of initial ;) contains the keyword
    echo !trimmedLine! | findstr /i /c:"%keyword%" >nul
    if errorlevel 1 (
        :: The keyword was not found, so write the line as is
        echo !line! >> "%outputFile%"
    ) else (
        :: The keyword was found, toggle comment
        if "!line:~0,1!" equ ";" (
            :: Line is commented, uncomment it
            echo !line:~1! >> "%outputFile%"
        ) else (
            :: Line is uncommented, comment it
            echo ;!line! >> "%outputFile%"
        )
    )
)

:: Replace the original file with the modified one
move /y "%outputFile%" "%inputFile%"

endlocal
echo Done.