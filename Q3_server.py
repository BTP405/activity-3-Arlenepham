import socket
import threading
import pickle

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []  # List of connected clients
        self.lock = threading.Lock()  # Lock for synchronization

    def handle_client(self, client_socket, client_address):
        try:
            with client_socket:
                self.clients.append(client_socket)
                print(f"New connection from {client_address}")

                while True:
                    pickled_message = client_socket.recv(1024)
                    if not pickled_message:
                        break

                    message = pickle.loads(pickled_message)
                    self.broadcast(message, client_socket)

        except (ConnectionError, EOFError):
            print("Error")
            pass
        finally:
            with self.lock:
                self.clients.remove(client_socket)
                print(f"Connection closed with {client_address}")

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(pickle.dumps(message))
                    except (ConnectionError, EOFError):
                        pass

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Chat server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer(host="127.0.0.1", port=3030)
    chat_server.start()
