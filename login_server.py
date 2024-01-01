#!/usr/bin/env python3
import socket
import threading
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute('''
        SELECT * FROM users
        WHERE username = ? AND password = ? AND active = 1
    ''', (username, hashed_password))
    return cursor.fetchone() is not None

def handle_client(client_socket):
    username = client_socket.recv(1024).decode()

    if check_user(username, "dummy_password"):  # Replace with actual password checking logic
        client_socket.sendall("SUCCESS".encode())
    else:
        client_socket.sendall("FAILURE".encode())

    client_socket.close()

def login_server():
    server_ip = '127.0.0.1'
    server_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)

        print(f"Login server listening on {server_ip}:{server_port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    conn = sqlite3.connect('user_accounts.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            active INTEGER
        )
    ''')
    conn.commit()

    login_server()
