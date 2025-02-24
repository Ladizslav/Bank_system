# Bankovní systém

## Základní informace
- **Jméno projektu:** Bankovní systém
- **Autor:** Ladislav Dobiáš
- **Datum dokončení:** 7.2.2025
- **Kontaktní údaje:** dobias@spsejecna.cz
- **Instituce:** Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
- **Typ projektu:** Školní projekt

## Příprava aplikace

1. **Stažení souborů:**
   - Soubory projektu si můžete stáhnout z Moodlu nebo z [GitHubu](https://github.com/Ladizslav/RDBMS-Lambda).

2. **Spuštění Visual Studio Code:**
   - Otevřete projekt ve Visual Studio Code.

3. **Vytvoření virtuálního prostředí a instalace závislostí:**
   - Otevřete terminál a zadejte následující příkazy:
     ```bash
     python -m venv venv
     cd ./venv/Scripts
     ./pip.exe install mysql-connector-python
     ```

## Nastavení MySQL

1. **Spuštění MySQL Workbench 8.0:**
   - Zkontrolujte, zda je vytvořeno základní připojení (Connection) s následující specifikací:
     - **User:** root
     - **Host:** localhost
     - **Port:** 3306

2. **Vytvoření nového připojení (pokud neexistuje):**
   - Klikněte na tlačítko `+` pro vytvoření nového připojení.
   - Nastavte Server Management přes "Configure Server Management".

3. **Nastavení `config.json`:**
   - Do souboru `config.json` vyplňte následující údaje:
     ```json
     {
       "host": "127.0.0.1",
       "user": "root",
       "password": "student",
       "database": "bank_db",
       "port": 3306
     }
     ```

## Spuštění aplikace

Aplikaci lze spustit dvěma způsoby:

1. **Ve Visual Studio Code:**
   - Otevřete soubor `main.py`.
   - Spusťte skript stisknutím klávesy `F5` nebo příkazem `Run`.

2. **Přímo ze souboru:**
   - Otevřete terminál.
   - Navigujte do složky, kde se nachází soubor `main.py`.
   - Spusťte příkaz:
     ```bash
     python main.py
     ```

## Jak aplikace funguje

Po spuštění aplikace se zobrazí menu s dostupnými příkazy, které můžete použít.

### Možnost 1: Použití Putty

1. **Spuštění Putty:**
   - Zadejte následující údaje:
     - **Host Name (or IP address):** 127.0.0.1
     - **Port:** 65525
     - **Connection type:** Raw

2. **Volitelné nastavení:**
   - **Close window on exit:** Never

3. **Použití:**
   - Po připojení můžete zadávat příkazy podle zobrazeného menu.

### Možnost 2: Přímé použití konzole

- Pokud nechcete používat Putty, můžete příkazy zadávat přímo v konzoli.

## Použité soubory z projektu

Aplikace využívá následující soubory z projektu [RDBMS-Lambda](https://github.com/Ladizslav/RDBMS-Lambda):

- `db/db_connector.py`
- `db/table_initiator.py`
- `config.json`
- `README.md`

---

**Poznámka:** Ujistěte se, že máte nainstalované všechny potřebné závislosti a že je správně nakonfigurován MySQL server před spuštěním aplikace.

## Použití AI

K apikaci jsem použil tyto AI:

- https://chat.deepseek.com/a/chat/s/37bb029f-bb76-41f9-887e-b29275a50b4c (README)
- https://chat.deepseek.com/a/chat/s/d17c6608-72cc-4abc-899f-682f98e83947 (Komentáře k bank_logic.py)