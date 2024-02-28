import socket
import pickle

def send_task(task_info, worder_nodes):
    try:
        for node in worder_nodes:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            client_socket.connect(node)
            
            #pickle and then send the task
            pickled_task = pickle.dumps(task_info)
            client_socket.sendall(pickled_task)
            print("Task sent successfully to:", node)

            # Receive result from the server
            receive_data = client_socket.recv(1024)
            print(f"Result received from {node}: {receive_data.decode()}", )

    except (ConnectionRefusedError, TimeoutError, OSError) as e:
        # Handle connection-related errors
        print(f"Error: {e}")
        return None

    finally:
        client_socket.close()

if __name__ == "__main__":
    def multiply_by_two(x):
        return x * 2
      
    task_info = {'function': multiply_by_two, 'args': (3,)}
  
    # example list of worker nodes
    worker_nodes = [('127.0.0.1',3030), ('127.4.6.2',8080)]

    result = send_task(task_info, worker_nodes)
    
    if result is not None:
        print(f"Result: {result}")
    else:
        print("Task execution failed.")
