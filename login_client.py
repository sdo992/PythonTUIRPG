#!/usr/bin/env python3
import hashlib
import curses
import curses.textpad  # Added import for textpad
import socket
import sqlite3
import time
import sys
import os

# Create a SQLite database connection
conn = sqlite3.connect('user_accounts.db')
cursor = conn.cursor()

# Create a table to store user accounts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        active INTEGER
    )
''')
conn.commit()

# Function to hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user account
def create_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute('''
        INSERT INTO users (username, password, active)
        VALUES (?, ?, ?)
    ''', (username, hashed_password, 1))
    conn.commit()

# Function to check if a user exists and is active
def check_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute('''
        SELECT * FROM users
        WHERE username = ? AND password = ? AND active = 1
    ''', (username, hashed_password))
    return cursor.fetchone() is not None

# Function to pass the user to the login server
def pass_user_to_login_server(username, password):
    login_server_ip = '127.0.0.1'  # Replace with the actual login server IP
    login_server_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as login_socket:
        login_socket.connect((login_server_ip, login_server_port))
        login_socket.sendall(username.encode())
        result = login_socket.recv(1024).decode()

        if result == "SUCCESS":
            print("Login successful!")
            pass_user_to_world_server(username)
        else:
            print("Login failed. Please check your username and password.")

# Function to pass the user to the world server
def pass_user_to_world_server(username):
    world_server_ip = '127.0.0.1'  # Replace with the actual world server IP
    world_server_port = 12346

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as world_socket:
        world_socket.connect((world_server_ip, world_server_port))
        world_socket.sendall(username.encode())
        result = world_socket.recv(1024).decode()

        if result == "Connected!":
            print("User connected to the world server.")
        else:
            print("User not connected to the world server.")

# Function to get user input with backspace support
def get_input_with_backspace(win, prompt, echo=True, password_field=False):
    if not echo:
        curses.noecho()
        curses.cbreak()
    else:
        win.timeout(-1)

    input_text = ""
    cursor_y, cursor_x = win.getyx()

    win.addstr(cursor_y, cursor_x, prompt)
    cursor_x += len(prompt)
    win.move(cursor_y, cursor_x)
    win.refresh()

    while True:
        ch = win.get_wch()

        if ch == 10:  # Enter key
            if input_text.strip():  # Check if input is not empty
                break
        elif ch == curses.KEY_BACKSPACE or ch == '\b' or ch == '\x7f':  # Backspace key
            if cursor_x > len(prompt):  # Check if cursor is after the prompt
                cursor_x -= 1
                win.addch(cursor_y, cursor_x, ' ')
                win.move(cursor_y, cursor_x)
                input_text = input_text[:-1]
        elif 32 <= ord(ch) <= 126:  # Printable ASCII characters
            input_text += ch
            cursor_x += 1
            if password_field:
                win.addch(cursor_y, cursor_x - 1, '*')
            else:
                win.addch(cursor_y, cursor_x - 1, ch)

        win.move(cursor_y, cursor_x)
        win.refresh()

    if not echo:
        curses.cbreak()
        curses.echo()

    return input_text.strip()  # Return input text with leading and trailing whitespaces removed

# Function to create a user entry box
def create_user_entry_box(win, prompt, y, x, width, password_field=False):
    while True:
        prompt += " "
        win.addstr(y, x, prompt)
        win.refresh()

        curses.curs_set(1)  # Show cursor
        curses.echo()
        input_text = ""
        cursor_x = x + len(prompt)

        while True:
            ch = win.get_wch()

            if ch == '\n' or ch == curses.KEY_ENTER:  # Enter key
                break
            elif ch == curses.KEY_BACKSPACE or ch == '\b' or ch == '\x7f':  # Backspace key
                if cursor_x > x + len(prompt):
                    cursor_x -= 1
                    win.addch(y, cursor_x, ' ')
                    input_text = input_text[:-1]
            elif isinstance(ch, str):
                if 32 <= ord(ch) <= 126:  # Printable ASCII characters
                    input_text += ch
                    win.addch(y, cursor_x, '*' if password_field else ch)
                    cursor_x += 1

            # Ensure cursor stays within the entry box
            if cursor_x >= x + len(prompt) + width:
                cursor_x = x + len(prompt) + width - 1

            win.move(y, cursor_x)
            win.refresh()

        curses.curs_set(0)  # Hide cursor
        curses.noecho()

        # Check if both username and password are non-empty
        if input_text.strip():
            return input_text.strip()
        else:
            # Display error message and restart the loop
            win.addstr(y + 2, x, "Error: Username or password cannot be empty!")
            win.refresh()
            time.sleep(3)  # Wait for 3 seconds
            win.addstr(y + 2, x, " " * 50)  # Clear error message
            win.refresh()

# Function to handle user creation
def create_user_handler(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 2, "Create User")
    stdscr.refresh()

    username_prompt = "Enter username:"
    password_prompt = "Enter password:"

    # Get non-empty username
    username = create_user_entry_box(stdscr, username_prompt, 4, 2, 20)
    while not username.strip():  # Keep asking until a non-empty username is provided
        stdscr.addstr(8, 2, "Error: Username cannot be empty!")
        stdscr.refresh()
        time.sleep(3)  # Wait for 3 seconds
        stdscr.addstr(8, 2, " " * 30)  # Clear error message
        stdscr.refresh()
        username = create_user_entry_box(stdscr, username_prompt, 4, 2, 20)

    # Get non-empty password
    password = create_user_entry_box(stdscr, password_prompt, 6, 2, 20, password_field=True)
    while not password.strip():  # Keep asking until a non-empty password is provided
        stdscr.addstr(10, 2, "Error: Password cannot be empty!")
        stdscr.refresh()
        time.sleep(3)  # Wait for 3 seconds
        stdscr.addstr(10, 2, " " * 30)  # Clear error message
        stdscr.refresh()
        password = create_user_entry_box(stdscr, password_prompt, 6, 2, 20, password_field=True)

    # Add your logic to handle the username and password as needed
    create_user(username, password)
    stdscr.addstr(12, 2, "User created successfully! Returning to main menu...")
    stdscr.refresh()
    time.sleep(3)  # Wait for 3 seconds

    # Return to the main menu
    main(stdscr)

# Function to handle user login
def login_handler(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 2, "Login")
    stdscr.refresh()

    username_prompt = "Enter username:"
    password_prompt = "Enter password:"

    username = create_user_entry_box(stdscr, username_prompt, 4, 2, 20)
    password = create_user_entry_box(stdscr, password_prompt, 6, 2, 20, password_field=True)

    # Add logic to handle the username and password as needed
    if username and password:
        if check_user(username, password):
            stdscr.addstr(8, 2, "Login successful!")
            pass_user_to_world_server(username)
        else:
            stdscr.addstr(8, 2, "Login failed. Please check your username and password.")
            stdscr.addstr(10, 2, "Hit 'Enter' to try again.")
            #time.sleep(2) # Wait for an arbitrary amount of time in seconds
    else:
        stdscr.addstr(8, 2, "Error: Username or password cannot be empty!")

    stdscr.refresh()
    stdscr.getch()  # Wait for user input

# Function to get user input for menu selection
def get_menu_choice(stdscr):
    curses.cbreak() # Disable line buffering
    curses.echo() # Enable echoing
    stdscr.clear()
    display_menu(stdscr)
    stdscr.move(6, 21)
    choice = stdscr.getch()  # Read a single character
    return chr(choice) if 32 <= choice <= 126 else ''  # Convert ASCII to character
    curses.noecho()    # Disable echoing
    curses.nocbreak()  # Enable line buffering

# Function to display the main menu
def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 2, "1. Create User")
    stdscr.addstr(3, 2, "2. Login")
    stdscr.addstr(4, 2, "3. Quit")
    stdscr.addstr(6, 2, "Choose an option: ")
    stdscr.refresh()

# Main function to run the login app
def main(stdscr):
    while True:
        choice = get_menu_choice(stdscr)

        if choice == '1':
            create_user_handler(stdscr)
        elif choice == '2':
            login_handler(stdscr)
        elif choice == '3':
            os.system('clear') # clear the screen
            curses.curs_set(0)  # Hide cursor
            print("Goodbye!")
            time.sleep(2)
            sys.exit(0) # Exit cleanly

if __name__ == "__main__":
    curses.wrapper(main)
