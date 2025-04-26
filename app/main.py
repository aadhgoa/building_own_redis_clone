# imports
import socket
import select

def handle_new_connection(server_socket, sockets_list, clients):
    """Handles a new connection to the server.
    Args:
        server_socket (socket.socket): The server socket.
        sockets_list (list): List of sockets to monitor for incoming connections.
        clients (dict): Dictionary of connected clients.
    """

    # Accept a new client and add it to the list of sockets
    client_socket, client_address = server_socket.accept()
    sockets_list.append(client_socket)
    clients[client_socket] = client_address
    print(f"Accepted new connection from {client_address}")


def handle_client_message(notified_socket, sockets_list, clients):
    """Handle message from the client.
    Args:
        client_socket (socket.socket): The socket of the client.
        socket_list (list): List of sockets to monitor for incoming connections.
        clients (dict): Dictionary of connected clients.
    """

    # Receive message from the client
    try:
        data = notified_socket.recv(1024)
        
        if not data:
            # If no data is received, the client has closed the connection
            print(f"Client {clients[notified_socket]} disconnected")
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
            notified_socket.close()
            return
        
        message = data.decode('utf-8').strip().upper()
        print(f"Received message from {clients[notified_socket]}: {message}")

        # If the message is "PING", send "PONG" back to the client 
        if message == "PING":
            notified_socket.sendall(b"+PONG\r\n")
        elif message == "EXIT":
            print(f"Client {clients[notified_socket]} requested to close the connection.")
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
            notified_socket.close()
        else:
            print(f"Unknown message from {clients[notified_socket]}: {message}")
            notified_socket.sendall(b"-ERR Unknown command\r\n")
    
    except Exception as e:
        print(f"Error handling message from {clients[notified_socket]}: {e}")
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()

   
def main():
    """Main function to run the server."""

    print(f"Starting the redis server on port 8080")

    # Create a socket server with the option to reuse the port
    server_socket = socket.create_server(('localhost', 8080), reuse_port=True)

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server is listening on port 8080")

    # List of sockets to monitor for incoming connections
    sockets_list = [server_socket]

    # Dictionary to keep track of connected clients
    clients = {}

    while True:
        # Use select to wait for incoming connections or messages
        try:
            read_sockets, _, _ = select.select(sockets_list, [], [])
        
            for notified_socket in read_sockets:
                # If the notified socket is the server socket, it means a new connection
                if notified_socket == server_socket:
                    handle_new_connection(server_socket, sockets_list, clients)
                else:
                    # Handle message from the client
                    handle_client_message(notified_socket, sockets_list, clients)

        except KeyboardInterrupt:
            print("Server shutting down...")
            break

        except Exception as e:
            print(f"Server error: {e}")
            break

    server_socket.close()
    print("Server closed.")

if __name__ == "__main__":
    main()

# This is a simple Redis-like server that handles PING and EXIT commands.
# It uses the select module to handle multiple clients concurrently.
# The server listens for incoming connections and responds to PING with PONG.
# It also handles client disconnections and unknown commands.
