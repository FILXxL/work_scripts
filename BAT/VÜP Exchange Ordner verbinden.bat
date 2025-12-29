@echo off &title "VÜP Exchange Ordner verbinden"

set exchange_default_buchstabe="Z"
set /p exchange_buchstabe="Welcher Laufwerksbuchstabe fuer den ExchangeOrdner?:"
set /p password="Bitte gib das Passwort ein, das du erhalten hast:"
if %exchange_buchstabe%=="" set exchange_buchstabe=%exchange_default_buchstabe%

REM Remove existing connection first if it exists
net use %exchange_buchstabe%: /delete /y >nul 2>&1

REM Add credentials to credential manager (overwrite if exists)
cmdkey /add:\\10.123.0.41\exchange /user:sd0402206\0402206_parkexchange /pass:%password% /generic

REM Mount the network share with persistent connection
net use %exchange_buchstabe%: \\10.123.0.41\exchange /persistent:yes

echo ExchangeOrdner als Laufwerk %exchange_buchstabe% eingerichtet.