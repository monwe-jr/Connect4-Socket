import socket
import threading

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #use IPV4, and stream (think TCP)
server.bind(("localhost", 2046)) #Normally we'd use use the proper host name
server.listen(5) #Allow up to 5 queued connections

def polite_chatter(client_one, client_two):
    while True:
        one_to_two=client_one.recv(100)
        if len(one_to_two)==0:
            break
        client_two.sendall(one_to_two)
        two_to_one=client_two.recv(100)
        if len(two_to_one)==0:
            break
        client_one.sendall(two_to_one)

while True: #Just keep accepting pairs of connections!
    (client_one, add_one) = server.accept()
    print("Accepted client A:"+str(add_one))
    (client_two, add_two) = server.accept()
    print("Accepted client B:"+str(add_two))
    threading.Thread(target=polite_chatter,args=(client_one,client_two)).start()