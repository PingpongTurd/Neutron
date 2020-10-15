import socket
import json
import threading
#data sent to server should be a list of 2, 1st value contains name, 2nd with a score!
def receive():
    while True: 
        conn, addr = server.accept() 
        clients[conn] = {}
        clients[conn]['CLIENT'] = conn
        clients[conn]['IP'] = addr 
        clients[conn]['DATA'] = list(conn.recv(8000).decode('utf-8'))
        if len(list(clients[conn]['DATA'])) != 2:
            clients[conn]["CLIENT"].close()
            del clients[conn]
        else:
            data={clients[conn]['DATA'][0]:clients[conn]['DATA'][1]}
            with open('glb.json',"r") as f:
                clb = json.load(f)
            clb.append(data)
            with open('glb.json','w') as f:
                json.dump(clb,f)
            clients[conn]["CLIENT"].close()
            del clients[conn]


while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = ""
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
