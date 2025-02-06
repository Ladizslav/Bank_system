import socket
import threading
from config import PORT, TIMEOUT, IP
from db_utils import get_connection, create_tables_and_views, create_account, deposit, withdraw, get_balance, delete_account, get_total_amount, get_client_count

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

import time

def handle_client(conn, addr):
    conn.settimeout(TIMEOUT)  # Nastavení timeoutu
    try:
        with conn.makefile('r') as f:
            last_ping_time = time.time()  # Čas posledního pingnutí
            while True:
                command = f.readline().strip()
                
                if not command:
                    if time.time() - last_ping_time > 60:
                        print(f"Zasílám ping na {addr}")
                        conn.sendall("PING\n".encode('utf-8'))
                        last_ping_time = time.time()  
                    continue  
                
                print(f"Přijatý příkaz: {command}")
                response = handle_command(command)
                conn.sendall((response + "\r\n").encode("utf-8"))
    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        conn.close()




def handle_command():
    while True:
        command = input("Zadejte příkaz: ").strip()

        if command.lower() == "exit":
            break
        
        parts = command.split()
        
        if not parts:
            print("ER Chyba: Prázdný příkaz.")
            continue

        code = parts[0]
        
        if code == "BC":
            print(f"BC {IP}")
        elif code == "AC":
            account_number = create_account(IP)
            if account_number:
                print(f"AC {account_number}/{IP}")
            else:
                print("ER Naše banka nyní neumožňuje založení nového účtu.")
        elif code == "AD":
            if len(parts) < 3:
                print("ER Chyba: Neplatný formát příkazu.")
                continue
            account, amount = parts[1], int(parts[2])
            account_number = int(account.split("/")[0])
            if deposit(account_number, amount):
                print("AD")
            else:
                print("ER Chyba: Účet neexistuje nebo neplatná částka.")
        elif code == "AW":
            if len(parts) < 3:
                print("ER Chyba: Neplatný formát příkazu.")
                continue
            account, amount = parts[1], int(parts[2])
            account_number = int(account.split("/")[0])
            if withdraw(account_number, amount):
                print("AW")
            else:
                print("ER Není dostatek finančních prostředků.")
        elif code == "AB":
            if len(parts) < 2:
                print("ER Chyba: Neplatný formát příkazu.")
                continue
            account = parts[1]
            account_number = int(account.split("/")[0])
            balance = get_balance(account_number)
            if balance is not None:
                print(f"AB {balance}")
            else:
                print("ER Chyba: Účet neexistuje.")
        elif code == "AR":
            if len(parts) < 2:
                print("ER Chyba: Neplatný formát příkazu.")
                continue
            account = parts[1]
            account_number = int(account.split("/")[0])
            if delete_account(account_number):
                print("AR")
            else:
                print("ER Nelze smazat bankovní účet na kterém jsou finance.")
        elif code == "BA":
            total_amount = get_total_amount()
            print(f"BA {total_amount}")
        elif code == "BN":
            client_count = get_client_count()
            print(f"BN {client_count}")
        else:
            print("ER Chyba: Neznámý příkaz.")
