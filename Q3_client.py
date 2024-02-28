import socket
import pickle
import threading

def receive_messages(client_socket):
    while True:
        try:
            pickled_message = client_socket.recv(1024)
            if not pickled_message:
                break

            message = pickle.loads(pickled_message)
            print(f"Received: {message}")
            
        except (ConnectionError, EOFError):
            print("Error")
            break
        
if __name__ == "__main__":
        server_address = ("127.0.0.1", 3030)
        client_socket=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            user_input = input("Enter your message: ")
            client_socket.sendall(pickle.dumps(user_input))
