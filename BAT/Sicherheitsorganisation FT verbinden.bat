@echo off &title "Sicherheitsorganisation FT verbinden"

set exchange_default_buchstabe="Z"
set /p exchange_buchstabe="Welcher Laufwerksbuchstabe fuer den Ordner?:"

if %exchange_buchstabe%=="" set %exchange_buchstabe%=%exchange_default_buchstabe%
net use %exchange_buchstabe%: /delete
net use %exchange_buchstabe%: "\\n3000\tt\Sicherheitsorganisation FT" /persistent:yes
echo "ExchangeOrdner als Laufwerk %vexchange_buchstabe% eingerichtet."