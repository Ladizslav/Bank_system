import socket
import threading
from config import PORT, TIMEOUT, IP
from db_utils import get_connection, create_tables_and_views, create_account, deposit, withdraw, get_balance, delete_account, get_total_amount, get_client_count, is_valid_user
import time

# Spustí bankovní uzel
def start_bank_node():
    connection = get_connection()
    if connection:
        create_tables_and_views(connection)  # Vytvoří DB tabulky
        connection.close()

    server_thread = threading.Thread(target=start_server)  # Spustí server
    server_thread.start()

    while True:
        command = input("Zadejte příkaz: ").strip()  # Čte příkazy z konzole
        if command.lower() == "exit":
            break
        response = handle_command(command)  # Zpracuje příkaz
        print(response)

# Naslouchá na IP a portu
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"Banka naslouchá na {IP}:{PORT}")

    while True:
        conn, addr = server.accept()  # Přijímá klienty
        print(f"Připojení od {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()  # Zpracuje klienta

# Zpracuje komunikaci s klientem
def handle_client(conn, addr):
    conn.settimeout(TIMEOUT)
    try:
        with conn.makefile('r') as f:
            while True:
                try:
                    command = f.readline().strip()  # Čte příkaz od klienta
                    if not command:
                        continue

                    print(f"Přijatý příkaz: {command}")
                    response = handle_command(command)  # Zpracuje příkaz
                    if response == "EXIT":
                        print(f"Klient {addr} ukončil spojení.")
                        conn.sendall("EXIT\r\n".encode("utf-8"))  # Ukončí spojení
                        break
                    conn.sendall((response + "\r\n").encode("utf-8"))  # Odešle odpověď
                except socket.timeout:
                    print(f"Timeout u klienta {addr}")
                    break
                except Exception as e:
                    print(f"Chyba u klienta {addr}: {e}")
                    break
    except Exception as e:
        print(f"Chyba komunikace: {e}")
    finally:
        conn.close()  # Uzavře spojení
        print(f"Spojení s {addr} ukončeno")

# Zpracuje příkazy
def handle_command(command):
    parts = command.split()
    
    if not parts:
        return "ER Chyba: Prázdný příkaz."

    code = parts[0].upper()
    
    try:
        if code == "BC":
            return f"BC {IP}"  # Vrátí IP banky
        
        elif code == "AC":
            account_number = create_account(IP)  # Vytvoří účet
            if account_number:
                return f"AC {account_number}/{IP}"
            else:
                return "ER Chyba: Nelze vytvořit účet."
        
        elif code == "AD":
            if len(parts) < 3:
                return "ER Chyba: Neplatný formát."
            account, amount = parts[1], parts[2]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                amount = int(amount)

                if amount < 0:
                    return "ER Chyba: Negativní hodnota."
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Neplatný účet."
                
                if deposit(account_number, amount):  # Vloží peníze
                    return "AD"
                else:
                    return "ER Chyba: Neplatná částka."
            except ValueError:
                return "ER Chyba: Špatný formát."
        
        elif code == "AW":
            if len(parts) < 3:
                return "ER Chyba: Neplatný formát."
            account, amount = parts[1], parts[2]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                amount = int(amount)

                if amount < 0:
                    return "ER Chyba: Negativní hodnota."
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Neplatný účet."
                
                if withdraw(account_number, amount):  # Vybere peníze
                    return "AW"
                else:
                    return "ER Chyba: Nedostatek prostředků."
            except ValueError:
                return "ER Chyba: Špatný formát."
        
        elif code == "AB":
            if len(parts) < 2:
                return "ER Chyba: Neplatný formát."
            account = parts[1]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Neplatný účet."
                
                balance = get_balance(account_number)  # Získá zůstatek
                if balance is not None:
                    return f"AB {balance}"
                else:
                    return "ER Chyba: Účet neexistuje."
            except ValueError:
                return "ER Chyba: Špatný formát."
        
        elif code == "AR":
            if len(parts) < 2:
                return "ER Chyba: Neplatný formát."
            account = parts[1]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Neplatný účet."
                
                if delete_account(account_number):  # Smaže účet
                    return "AR"
                else:
                    return "ER Chyba: Nelze smazat účet."
            except ValueError:
                return "ER Chyba: Špatný formát."
        
        elif code == "BA":
            total_amount = get_total_amount()  # Získá celkový obnos
            return f"BA {total_amount}"
        
        elif code == "BN":
            client_count = get_client_count()  # Získá počet klientů
            return f"BN {client_count}"
        
        elif code == "EXIT":
            return "EXIT"  # Ukončí spojení
        
        else:
            return "ER Chyba: Neznámý příkaz."
    
    except Exception as e:
        return f"ER Chyba: {str(e)}"