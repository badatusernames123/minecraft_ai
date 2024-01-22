import socket
import threading
import pickle_tools

class CollectorServer:
    def __init__(self, host, port, callback=None, collection_data=dict(), recog_map=dict()):
        self.host = host
        self.port = port
        self.callback = callback
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.collection_data = collection_data
        self.recog_map = recog_map
        self.running = True

    def listen_for_clients(self):
        self.server.listen()
        try:
            while self.running:
                try:
                    client, address = self.server.accept()
                except socket.error as e:
                    # Break out of the loop if the server is no longer running
                    if not self.running:
                        break
                    else:
                        raise e
                    
                print(f"Connected to {address}")
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.running = False
        print('Updating Collection Data')
        pickle_tools.save_to_pickle(self.collection_data, 'mods/Collector/data/collection_data.pkl')
        
        print('Updating Recognition Map')
        pickle_tools.save_to_pickle(self.recog_map, 'mods/Collector/data/recog_map.pkl')

        print('Shutting down server')
        self.server.close()

    def handle_client(self, client):
        data_buffer = ''
        while True:
            data = client.recv(2048)
            if not data:
                break
            
            data_str = data.decode('utf-8')
            data_buffer += data_str
            if '\n' in data_buffer:
                complete_message, _, data_buffer = data_buffer.partition('\n')

                print(f"Received data: {complete_message}")

                if complete_message == '!DISCONNECT':
                    print(f"Disconnected")
                    self.shutdown()
                    break

                response = 'Data processed\n'
                client.sendall(response.encode('utf-8'))

                if self.callback:
                    self.callback(complete_message, self.collection_data, self.recog_map)

        client.close()

# Example usage
# ip = socket.gethostbyname(socket.gethostname())
# server = CollectorServer(ip, 5050)  # Use your desired IP and port
# server.listen_for_clients()
