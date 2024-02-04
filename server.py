import socket
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'  # Allow connections from any IP
SERVER_PORT = 8080
ADDR = (SERVER_HOST, SERVER_PORT)

# List to store connected clients
clients = []

# Get the server's IP address
ip_address = socket.gethostbyname(socket.gethostname())

# Socket creation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(client_socket, client_address, username):
    print(f"New connection from {client_address} with username {username}")

    # Print the client's IP address
    print(f"Client IP address: {client_address[0]}")

    while True:
        try:
            # Receive messages from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"Received message from {username}: {message}")

            # Check for the "exit" command
            if message.lower() == 'exit':
                broadcast(f"{username} has left the chat.")
                clients.remove((client_socket, client_address, username))
                client_socket.close()
                break

            # Broadcast the message to all connected clients
            broadcast(f"{username}: {message}")

        except Exception as e:
            print(f"Error handling client {username}: {e}")
            break

def broadcast(message):
    for client, address, username in clients:
        try:
            # Send the message to all clients
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error broadcasting to client {username}: {e}")
            # Remove disconnected clients
            clients.remove((client, address, username))
            client.close()

def start():
    print(f"Server is running on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        server.listen()
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")

        # Receive the username from the client
        username = client_socket.recv(1024).decode('utf-8')

        # Add the new client to the clients list
        clients.append((client_socket, client_address, username))

        # Start a new thread for each connected client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
        client_handler.start()

if __name__ == "__main__":
    print(f"Server IP address: {ip_address}")
    start()
