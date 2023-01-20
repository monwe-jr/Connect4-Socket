import socket

class Client:
    
    def __init__(self):
        self.client_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client_one.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_one.connect(("localhost", 3009))
        self.client_two = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client_two.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_two.connect(("localhost", 3009))


    def send(self, grid):
        self.client_one.sendall(grid.encode())
        self.client_two.sendall(grid.encode())


    def recieve_from_one(self):
        self.client_two.recv(1024)
        return self.client_one.recv(1024)
       
        
    def recieve_from_two(self):
        self.client_one.recv(1024)
        return self.client_two.recv(1024)
   

    def end(self):
        self.client_one.close()  
        self.client_two.close()   


    






















