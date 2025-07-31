# Simple Python CLI Chat Room
This is a simple, multi-client, command-line chat room application built with Python's native socket and threading libraries. It provides a basic framework for real-time communication between multiple users.

## Features
* Multi-Client Support: The server uses threading to handle multiple client connections simultaneously.
* Password Protected: Users must enter a correct password to join the chat room.
* Unique Usernames: The server ensures that every user has a unique username.
* Real-time Broadcasting: Messages sent by a user are instantly broadcast to all other users in the chat room.
* Server Admin Commands: The server has a simple command-line interface for administrative tasks like kicking users or shutting down the server.

## How It Works
The project consists of two main components:

* server.py: This script listens for incoming connections on a specified port. When a new client connects, it spawns a new thread to handle all communications with that client, including authentication, message broadcasting, and handling disconnects gracefully. It also has a separate thread for handling admin commands from the server's terminal.
* client.py: This script connects to the server. It uses two threads:
  1. A main thread to capture user input and send messages to the server.
  2. A background thread to continuously listen for and display incoming messages from the server.
