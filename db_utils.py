import mysql.connector
from mysql.connector import Error
import json

def get_connection():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)

        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            port=config["port"],
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"create database if not exists {config['database']};")
            cursor.execute(f"use {config['database']};")
            print("Connected successfully")
            return connection
        else:
            print("Failed to connect to database")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None

def create_tables_and_views(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_number INT NOT NULL UNIQUE,
        balance DECIMAL(15, 2) NOT NULL DEFAULT 0,
        ip VARCHAR(15) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """)
    connection.commit()
    print("Tabulky byly vytvořeny.")

def create_account(ip):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(account_number) FROM accounts;")
        max_account_number = cursor.fetchone()[0]
        account_number = max_account_number + 1 if max_account_number else 10000
        cursor.execute("INSERT INTO accounts (account_number, ip) VALUES (%s, %s);", (account_number, ip))
        connection.commit()
        connection.close()
        return account_number
    return None

def deposit(account_number, amount):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s;", (amount, account_number))
        connection.commit()
        connection.close()
        return True
    return False

def withdraw(account_number, amount):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s;", (account_number,))
        balance = cursor.fetchone()[0]
        if balance >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s;", (amount, account_number))
            connection.commit()
            connection.close()
            return True
        connection.close()
    return False

def get_balance(account_number):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s;", (account_number,))
        balance = cursor.fetchone()
        connection.close()
        return balance[0] if balance else None
    return None

def delete_account(account_number):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s;", (account_number,))
        balance = cursor.fetchone()[0]
        if balance == 0:
            cursor.execute("DELETE FROM accounts WHERE account_number = %s;", (account_number,))
            connection.commit()
            connection.close()
            return True
        connection.close()
    return False

def get_total_amount():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(balance) FROM accounts;")
        total_amount = cursor.fetchone()[0]
        connection.close()
        return total_amount or 0
    return 0

def get_client_count():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM accounts;")
        client_count = cursor.fetchone()[0]
        connection.close()
        return client_count
    return 0