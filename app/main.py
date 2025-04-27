# imports
import socket
import select
import time

# Response messages
OK_RESPONSE = b"+OK\r\n"
INVALID_SET_FORMAT_RESPONSE = b"-ERR Invalid SET command format\r\n"
INVALID_GET_FORMAT_RESPONSE = b"-ERR Invalid GET command format\r\n"
INVALID_EXIT_FORMAT_RESPONSE = b"-ERR Invalid EXIT command format\r\n"
UNKNOWN_COMMAND_RESPONSE = b"-ERR Unknown command\r\n"
NIL_RESPONSE = b"$-1\r\n"

def handle_new_connection(server_socket, sockets_list, clients):
    """
    Handles a new connection to the server.

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


def handle_client_message(notified_socket, sockets_list, clients, memory):
    """
    Handle message from the client.

    Args:
        notified_socket (socket.socket): The socket of the client.
        socket_list (list): List of sockets to monitor for incoming connections.
        clients (dict): Dictionary of connected clients.
        memory (dict): Dictionary to store key-value pairs in memory.
    This function handles the message received from the client.
    It checks the command and performs the appropriate action.
    It supports the following commands:
        - SET key value: Store the key-value pair in memory.
        - GET key: Retrieve the value by key from memory.
        - EXIT: Close the connection.
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

        # Handle SET command (store key-value pairs)
        if message.startswith("SET"):
            # Check if the message is in the correct format
            if len(message.split()) < 3:
                notified_socket.sendall(INVALID_SET_FORMAT_RESPONSE)
                return 
            
            # Extract key and value from the message
            # Example: SET key value EX 10

            # Split the message into parts
            # Example: SET key value EX 10
            parts = message.split()

            if len(parts) == 3:
                _, key, value = parts
                ttl = None

            elif len(parts) == 5 and parts[3] == "EX":
                _, key, value, _, ttl = parts
            
            else:
                notified_socket.sendall(INVALID_SET_FORMAT_RESPONSE)
                return
            # Store the key-value pair in the memory dictionary
            if key in memory:
                notified_socket.sendall(b"-ERR Key already exists\r\n")
                return 
            if not value:
                notified_socket.sendall(b"-ERR Value cannot be empty\r\n")
                return
            if not key:
                notified_socket.sendall(b"-ERR Key cannot be empty\r\n")
                return
            

            # Store the key-value pair along with the expiration time
            # Example: SET key value EX 10
            if ttl:
                try:
                    ttl = int(ttl)
                    if ttl <= 0:
                        notified_socket.sendall(b"-ERR Invalid TTL value\r\n")
                        return
                    
                    # Calculate the expiration time
                    expiry_time = time.time() + ttl

                    # Store the key-value pair with the expiration time
                    memory[key] = {'value': value, 'expiry_time': expiry_time}
                except ValueError:
                    notified_socket.sendall(b"-ERR Invalid TTL value\r\n")
                    return 
            else:
                # Store the key-value pair without expiration
                memory[key] = {'value': value, 'expiry_time': None}
            print(f"Stored key-value pair: {key} -> {value}")
            # Send success response to the client
            notified_socket.sendall(OK_RESPONSE)

        # Handle GET command (retrieve value by key)
        elif message.startswith("GET"):
            # Check if the message is in the correct format
            if len(message.split()) != 2:
                notified_socket.sendall(INVALID_GET_FORMAT_RESPONSE)
                return 
            
            # Extract key from the message
            # Example: GET key
            _, key = message.split()

            # Retrieve the value from the memory dictionary
            if key in memory:
                # Check if the key has expired
                if memory[key]['expiry_time'] is not None and time.time() > memory[key]['expiry_time']:
                    # Key has expired, remove it from memory
                    del memory[key]
                    notified_socket.sendall(NIL_RESPONSE)
                    return 
                # Key is valid, retrieve the value
                # Example: GET key
                # Send the value to the client
                value = memory[key]['value']
                notified_socket.sendall(f"${len(value)}\r\n{value}\r\n".encode('utf-8'))
            else:
                notified_socket.sendall(NIL_RESPONSE)
        
        # Handle EXIT command (close the connection)
        elif message.startswith("EXIT"):
            # Check if the message is in the correct format
            if len(message.split()) != 1:
                notified_socket.sendall(INVALID_EXIT_FORMAT_RESPONSE)
                return 
            
            # Close the connection
            print(f"Client {clients[notified_socket]} requested to close the connection.")
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
            notified_socket.close()
            return
        
        else:
            notified_socket.sendall(UNKNOWN_COMMAND_RESPONSE)
        
    except Exception as e:
        print(f"Error handling message from {clients[notified_socket]} : {e}")
        # If an error occurs, close the connection
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

    # Dictionary to store key-value pairs in memory
    memory = {}



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
                    handle_client_message(notified_socket, sockets_list, clients, memory)

        except KeyboardInterrupt:
            print("Server shutting down...")
            break

        except Exception as e:
            print(f"Server error: {e}")
            for sock in sockets_list:
                sock.close()
            print("Server closed.")
            break


if __name__ == "__main__":
    main()

# This is a simple Redis-like server that handles PING and EXIT commands.
# It uses the select module to handle multiple clients concurrently.
# The server listens for incoming connections and responds to PING with PONG.
# It also handles client disconnections and unknown commands.
