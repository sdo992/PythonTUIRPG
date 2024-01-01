#!/usr/bin/env python3
import socket
import time

def world_server():
    server_ip = '127.0.0.1'
    server_port = 12346

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)  # Listen for one incoming connection

        print(f"World server listening on {server_ip}:{server_port}")

        while True:
            user_socket, user_address = server_socket.accept()
            print(f"User connected from {user_address}")

            user_socket.sendall("Connected!".encode())

            time.sleep(3)

            user_socket.close()
            print("User disconnected")

if __name__ == "__main__":
    world_server()
