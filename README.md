# Bank_system
- Jméno projektu: Bankovní systém
- Autor: Ladislav Dobiáš
- Datum dokončení: 7.2.2025
- Kontaktní údaje: dobias@spsejecna.cz
- Instituce: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
- Typ projektu: Školní projekt

## Příprava aplikace

1. Stáhněte soubor z Moodlu nebo z GitHubu.
2. Spusťte Visual Studio Code.
3. Otevřete terminál a zadejte příkaz:

    python -m venv venv
    cd ./venv/Scripts
    ./pip.exe install mysql-connector-python

---
        
## Nastavení MySQL
        
1. Spusťte aplikaci **MySQL Workbench 8.0**.
2. Zkontrolujte, zda je vytvořeno základní připojení (Connection) se specifikací:

    User: root
    Host: localhost 
    Port: 3306

3. Pokud připojení neexistuje:
- Klikněte na tlačítko `+` pro vytvoření nového připojení.
- Nastavte `Server Management` přes "Configure Server Management".
4. **Poznámka:** 
- Je nuté vyplnit data do config.json.
- Tady jsou moje použite:

{
    "host": "127.0.0.1",
    "user": "root",
    "password": "student",
    "database": "bank_db",
    "port": 3306
}
      
---

## Spuštění aplikace
        
Aplikaci lze spustit dvěma způsoby:
        
### Ve Visual Studio Code
1. Otevřete soubor `main.py`.
2. Spusťte skript stisknutím klávesy `F5` nebo příkazem `Run`.
        
### Přímo ze souboru
1. Otevřete terminál.
2. Navigujte do složky, kde se nachází soubor `main.py`.
3. Spusťte příkaz:

    python main.py

---

## Jak aplikace funguje

Po spuštění aplikace se zobrazí menu s dostupnými příkazy, které můžete použít.

### Možnost 1: Použití Putty

1. Spusťte **Putty** a zadejte následující údaje:
   - **Host Name (or IP address):** `127.0.0.1`
   - **Port:** `65525`
   - **Connection type:** `Raw`

2. Volitelně můžete nastavit:
   - **Close window on exit:** `Never`

3. Po připojení můžete zadávat příkazy podle zobrazeného menu.

### Možnost 2: Přímé použití konzole

Pokud nechcete používat Putty, můžete příkazy zadávat přímo v konzoli.

## Použité soubory z projektu

Aplikace využívá následující soubory z projektu **[RDBMS-Lambda](https://github.com/Ladizslav/RDBMS-Lambda)**:
    
    db/db_connector.py 
    db/table_initiator.py 
    config.json 
    README.md

