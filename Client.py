import socket

class Client:
    
    def __init__(self):
        self.client_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client_one.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_one.connect(("localhost", 3006))
        self.client_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client_two.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_two.connect(("localhost", 3006))


    def send(self, grid):
        try:
            self.client_one.sendall(grid.encode())
            self.client_two.sendall(grid.encode())
        except: #For EOF on ctrl+d or interrupt on ctrl+c
            self.client.shutdown(1)
            self.client.close()       


    def recieve_from_one(self):
        r =self.client_one.recv(100)
        return r
        
    
    def recieve_from_two(self):
        r =self.client_two.recv(100)
        return r
   
    






















