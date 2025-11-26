@echo off &title "VÜP Exchange Ordner verbinden"

set exchange_default_buchstabe="Z"
set /p exchange_buchstabe="Welcher Laufwerksbuchstabe fuer den ExchangeOrdner?:"
set /p password="Bitte gib das Passwort ein, das du erhalten hast:"
if %exchange_buchstabe%=="" set %exchange_buchstabe%=%exchange_default_buchstabe%
net use %exchange_buchstabe%: /delete
net use %exchange_buchstabe%: \\10.123.0.41\exchange %password% /user:sd0402206\0402206_parkexchange /persistent:yes
echo "ExchangeOrdner als Laufwerk %vexchange_buchstabe% eingerichtet."