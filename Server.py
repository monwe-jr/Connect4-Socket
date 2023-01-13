import socket
import threading

class Server:

    def __init__(self):
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.bind(("localhost", 2046)) 
        self.server.listen(5) #Allow up to 5 queued connections
        while True: 
            (client_one, add_one) = self.server.accept()
            print("Accepted client A:"+str(add_one))
            (client_two, add_two) = self.server.accept()
            print("Accepted client B:"+str(add_two))
            threading.Thread(target=self.encoder,args=(client_one,client_two)).start()


    def encoder(self, client_one, client_two):
        while True:
            one_to_two=client_one.recv(100)
            if len(one_to_two)==0:
                break
            client_two.sendall(one_to_two)
            two_to_one=client_two.recv(100)
            if len(two_to_one)==0:
                break
            client_one.sendall(two_to_one)

   