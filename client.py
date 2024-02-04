import socket
import threading

# Prompt the user for the server's IP address or hostname
SERVER = input("Enter the server's IP address: ")
PORT = 8080  # Change this to the port number your friend's server is using
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
    print(f"Connected to {SERVER}:{PORT}")

    # Ask the user for their username
    username = input("Enter your username: ")
    client.send(username.encode('utf-8'))
    print(f"You have entered the chat as {username}")

    def receive_messages():
        while True:
            try:
                # Receive messages from the server
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break

                # Print the received message
                print(message)

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    # Start a new thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Your client logic goes here
    while True:
        message = input("")
        client.send(message.encode('utf-8'))

        # Check for the exit command
        if message.lower() == 'exit':
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    client.close()
