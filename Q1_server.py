import socket
import pickle
import os

def run_server(save_path):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1',3030 )
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Server is listening for connection...")
        
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print("Connected to: ", client_address)
                pickled_file = client_socket.recv(4096)
                
                 # Unpickle the file and save it to disk
                file_data = pickle.loads(pickled_file)
                save_directory = input("Input your saving directory: ")
                file_name = os.path.basename(save_directory) #extracts the file name without the directory path)
                save_path = os.path.join(save_directory, file_name) #create the complete save path for the received file
                
                with open(save_path, "wb") as file:
                    file.write(file_data)
                print(f"File saved at: {save_path}")
                
            except (ConnectionResetError, ConnectionAbortedError):
                print("Error: Connection with client was unexpectedly closed.")
            except FileNotFoundError:
                print(f"Error: Save directory '{save_directory}' not found.")
            except OSError as e:
                print(f"Error while receiving file: {e}")

    finally:
        server_socket.close()
        
if __name__ == "__main__":
    run_server()
