import socket
import json
import threading
import pickle
#data sent to server should be a list of 2, 1st value contains name, 2nd with a score!
def receive():
    while True: 
        conn, addr = server.accept() 
        clients[conn] = {}
        clients[conn]['CLIENT'] = conn
        clients[conn]['IP'] = addr 
        clients[conn]['DATA'] = list(pickle.loads(conn.recv(8000)))
        print(len(clients[conn]['DATA']))
        print(clients[conn]['DATA'])
        if len(clients[conn]['DATA']) != 2:
            clients[conn]["CLIENT"].close()
            del clients[conn]
            print("Invalid data sent, connection closed")
        else:
            with open('glb.json',"r") as f:
                clb = json.load(f)
            clb[clients[conn]['DATA'][0]] = clients[conn]['DATA'][1]
            print(clb)
            with open('glb.json','w') as f:
                json.dump(clb,f)
            clients[conn]["CLIENT"].close()
            del clients[conn]


while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "192.168.1.100"
    port = 8888
    try: 
        server.bind((ip,port))
    except socket.error as e:
        print(str(e)) 
    server.listen() 

    clients = {}

    a = threading.Thread(target=receive)
    a.start()
    a.join()
