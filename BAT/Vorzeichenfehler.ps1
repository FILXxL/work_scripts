$iniFilePath = "C:\Orbis\sql.ini"
$iniContent = Get-Content -Path $iniFilePath
$lineFoundAndModified = $false
$commentPattern = "^\s*;.*log=C:\\Temp\\oracle.log\s*$"
$uncommentPattern = "^\s*log=C:\\Temp\\oracle.log\s*$"

foreach ($line in $iniContent) {
    if ($line -match $commentPattern) {
        $iniContent[$iniContent.IndexOf($line)] = $line.TrimStart(";")
        $lineFoundAndModified = $true
        break
    }
    elseif ($line -match $uncommentPattern) {
        $iniContent[$iniContent.IndexOf($line)] = ";$line"
        $lineFoundAndModified = $true
        break
    }
}

if ($lineFoundAndModified) {
    $iniContent | Set-Content -Path $iniFilePath
    Write-Host "The specified line was successfully toggled."
} else {
    Write-Host "The specified line was not found in the file."
}
