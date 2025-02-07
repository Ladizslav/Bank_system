import socket
import threading
from config import PORT, TIMEOUT, IP
from db_utils import get_connection, create_tables_and_views, create_account, deposit, withdraw, get_balance, delete_account, get_total_amount, get_client_count, is_valid_user
import time

def start_bank_node():
    connection = get_connection()
    if connection:
        create_tables_and_views(connection)
        connection.close()

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    while True:
        command = input("Zadejte příkaz: ").strip()
        if command.lower() == "exit":
            break
        response = handle_command(command)
        print(response)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"Banka naslouchá na {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Připojení od {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def handle_client(conn, addr):
    conn.settimeout(TIMEOUT)
    try:
        with conn.makefile('r') as f:
            while True:
                try:
                    command = f.readline().strip()
                    if not command:
                        continue

                    print(f"Přijatý příkaz: {command}")
                    response = handle_command(command)
                    if response == "EXIT":
                        print(f"Klient {addr} ukončil spojení.")
                        conn.sendall("EXIT\r\n".encode("utf-8"))
                        break
                    conn.sendall((response + "\r\n").encode("utf-8"))
                except socket.timeout:
                    print(f"Timeout u klienta {addr}")
                    break
                except Exception as e:
                    print(f"Chyba při zpracování příkazu od {addr}: {e}")
                    break
    except Exception as e:
        print(f"Chyba při komunikaci s klientem {addr}: {e}")
    finally:
        conn.close()
        print(f"Spojení s {addr} ukončeno")

def handle_command(command):
    parts = command.split()
    
    if not parts:
        return "ER Chyba: Prázdný příkaz."

    code = parts[0].upper()
    
    try:
        if code == "BC":
            return f"BC {IP}"
        
        elif code == "AC":
            account_number = create_account(IP)
            if account_number:
                return f"AC {account_number}/{IP}"
            else:
                return "ER Chyba: Naše banka nyní neumožňuje založení nového účtu."
        
        elif code == "AD":
            if len(parts) < 3:
                return "ER Chyba: Neplatný formát příkazu."
            account, amount = parts[1], parts[2]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                amount = int(amount)

                if amount < 0:
                    return "ER Chyba: Nemůžeš dát negativní hodnotu"
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Účet neexistuje nebo nepatří k této bance."
                
                if deposit(account_number, amount):
                    return "AD"
                else:
                    return "ER Chyba: Účet neexistuje nebo neplatná částka."
            except ValueError:
                return "ER Chyba: Číslo bankovního účtu a částka není ve správném formátu."
        
        elif code == "AW":
            if len(parts) < 3:
                return "ER Chyba: Neplatný formát příkazu."
            account, amount = parts[1], parts[2]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                amount = int(amount)

                if amount < 0:
                    return "ER Chyba: Nemůžeš dát negativní hodnotu"
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Účet neexistuje nebo nepatří k této bance."
                
                if withdraw(account_number, amount):
                    return "AW"
                else:
                    return "ER Chyba: Není dostatek finančních prostředků."
            except ValueError:
                return "ER Chyba: Číslo bankovního účtu a částka není ve správném formátu."
        
        elif code == "AB":
            if len(parts) < 2:
                return "ER Chyba: Neplatný formát příkazu."
            account = parts[1]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Účet neexistuje nebo nepatří k této bance."
                
                balance = get_balance(account_number)
                if balance is not None:
                    return f"AB {balance}"
                else:
                    return "ER Chyba: Účet neexistuje."
            except ValueError:
                return "ER Chyba: Formát čísla účtu není správný."
        
        elif code == "AR":
            if len(parts) < 2:
                return "ER Chyba: Neplatný formát příkazu."
            account = parts[1]
            try:
                account_number = int(account.split("/")[0])
                ip = account.split("/")[1]
                
                if not is_valid_user(account_number, ip):
                    return "ER Chyba: Účet neexistuje nebo nepatří k této bance."
                
                if delete_account(account_number):
                    return "AR"
                else:
                    return "ER Chyba: Nelze smazat bankovní účet na kterém jsou finance."
            except ValueError:
                return "ER Chyba: Formát čísla účtu není správný."
        
        elif code == "BA":
            total_amount = get_total_amount()
            return f"BA {total_amount}"
        
        elif code == "BN":
            client_count = get_client_count()
            return f"BN {client_count}"
        
        elif code == "EXIT":
            return "EXIT"
        
        else:
            return "ER Chyba: Neznámý příkaz."
    
    except Exception as e:
        return f"ER Chyba v aplikaci: {str(e)}"