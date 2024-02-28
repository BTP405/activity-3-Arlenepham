import socket
import pickle

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address= ('127.0.0.1',3030 )
    client_socket.connect(client_address )
        
    try:
        file_path = input("Input your file path: ")
        # Pickle the file object
        with open(file_path, 'rb') as file:
            file_data = pickle.dumps(file.read())
        client_socket.sendall(file_data)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except (ConnectionRefusedError, TimeoutError):
        print(f"Error: Could not connect to the server.")
    except Exception as e:
        print(f"Error while sending file: {e}")
        
        
    finally:
        client_socket.close()
        
if __name__ == "__main__":
    run_client()
