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
    create table if not exists accounts (
        id int auto_increment primary key,
        account_number int not null unique,
        balance decimal(15, 2) not null default 0,
        ip varchar(15) not null,
        created_at timestamp default current_timestamp,
        updated_at timestamp default current_timestamp on update current_timestamp
    );
    """)
    connection.commit()
    print("Tabulky byly vytvořeny.")

def create_account(ip):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select max(account_number) from accounts;")
        max_account_number = cursor.fetchone()[0]
        account_number = max_account_number + 1 if max_account_number else 10000
        cursor.execute("insert into accounts (account_number, ip) values (%s, %s);", (account_number, ip))
        connection.commit()
        connection.close()
        return account_number
    return None

def deposit(account_number, amount):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("update accounts set balance = balance + %s where account_number = %s;", (amount, account_number))
        connection.commit()
        connection.close()
        return True
    return False

def withdraw(account_number, amount):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select balance from accounts where account_number = %s;", (account_number,))
        balance = cursor.fetchone()[0]
        if balance >= amount:
            cursor.execute("update accounts set balance = balance - %s where account_number = %s;", (amount, account_number))
            connection.commit()
            connection.close()
            return True
        connection.close()
    return False

def get_balance(account_number):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select balance from accounts where account_number = %s;", (account_number,))
        balance = cursor.fetchone()
        connection.close()
        return balance[0] if balance else None
    return None

def delete_account(account_number):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select balance from accounts where account_number = %s;", (account_number,))
        balance = cursor.fetchone()[0]
        if balance == 0:
            cursor.execute("delete from accounts where account_number = %s;", (account_number,))
            connection.commit()
            connection.close()
            return True
        connection.close()
    return False

def get_total_amount():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select sum(balance) from accounts;")
        total_amount = cursor.fetchone()[0]
        connection.close()
        return total_amount or 0
    return 0

def get_client_count():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select count(*) from accounts;")
        client_count = cursor.fetchone()[0]
        connection.close()
        return client_count
    return 0