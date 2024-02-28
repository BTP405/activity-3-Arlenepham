import socket
import pickle
import threading

def handle_client(client_socket, client_address):
    try:
        print("Connected to", client_address)

        pickled_task = client_socket.recv(1024)
        task = pickle.loads(pickled_task)

        function = task.get('function')
        args = task.get('args')

        if callable(function) and isinstance(args, tuple):
            result = function(*args)
            # Send the result back to the client
            client_socket.sendall(str(result).encode())
            print("Task executed successfully")

        else:
            print("Invalid task format. Ignoring.")

    except (pickle.UnpicklingError, ConnectionResetError) as e:
        print(f"Failed to execute the task: {e}")

    finally:
        # Clean up the connection
        client_socket.close()

def execute_task(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 12345)  
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Server is listening for incoming connections...")
    execute_task(server_socket)
