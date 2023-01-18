import socket

class Client:
    global msg

    def __init__(self, board):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use IPV4
        self.client.connect(("localhost", 2046))
        while True:
            try:
                s=board
                self.client.sendall((s+"\n").encode())
                r=self.client.recv(100)
                self.msg = r.decode().strip()
            except: #For EOF on ctrl+d or interrupt on ctrl+c
                break 

    def recieve(self):
        return self.msg 
   























