#imports

import socket
import threading

def handle_client(connection, address):
    """Function to handle client connection.
    Args:
        connection (socket.socket): The client connection socket.
        address (tuple): The address of the client.
    """
    print(f"New connection from {address}")

    try:
    # Handle client connection
        while True:
        
            # Receive data from the client
            data = connection.recv(1024)

            if not data:
                print("No data received. Closing connection.")
                break
            print(f"Received data from {address}: {data.decode('utf-8')}")

            # Decode the data and strip the message
            message = data.decode('utf-8').strip().upper()

            # Check if the message is a PING message, respond with a PONG message else say UNKNOWN COMMAND
            if message == "PING":
                response = "PONG"
                connection.sendall(response.encode('utf-8'))
            else:
                response =  "UNKNOWN COMMAND"
                connection.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
        

    finally:
        # Close the connection 
        print(f"Closing connection from {address}")
        connection.close()

# Main function to start the server
def main():
    """Main function to start the server."""

    print("Starting Redis Clone server...")
    # Set the server to run in a separate thread

    # Create a server socket
    server_socket = socket.create_server(('localhost', 8080), reuse_port=True)

    # Set the server to listen for incoming connections
    server_socket.listen()

    print("Server is listening on port 8080...")

    # Accept incoming connections
    while True:
        try:
            # Accept a new connection
            connection, address = server_socket.accept()

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(connection, address))

            # Start the thread
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
        
        except KeyboardInterrupt:
            print("Server shutting down...")
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")
            break

    # Close the server socket
    server_socket.close()
    print("Server socket closed.")


if __name__ == "__main__":
    main()
# This is a simple Redis clone server that handles PING and PONG commands.
# It uses Python's socket and threading libraries to handle multiple clients concurrently.
# The server listens on localhost and port 8080.
# It accepts incoming connections and creates a new thread for each client.
# The server handles PING commands by responding with PONG and any other command with UNKNOWN COMMAND.
# The server can be stopped using a keyboard interrupt (Ctrl+C).
# The server is designed to be simple and easy to understand, making it a good starting point for learning about socket programming in Python.


    
