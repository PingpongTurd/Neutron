#Todo: https://trello.com/b/SFzvhiz6/tristan-invaders

import pygame
import socket
import pickle
import os
import time
import random
import threading

"""

OBJ ( WHAT IT TOUCHED, WHO TOUCHED IT )
SEL ( CLIENT AND ALL THE DATA IN SELF )

"""


def receive():
    while True: 
        conn, addr = server.accept() 
        clients[conn]['CLIENT'] = conn
        clients[conn]['IP'] = addr 
        recvd = list(pickle.loads(conn.recv(8000)))
        if recvd[1] == 'SEL':
            clients[onn]['USERANME'] = recvd[0]
            clients[conn]['POSITION'] = recvd[2]
            clients[conn]['HEALTH'] = recvd[3]
        elif recvd[1] == 'OBJ':
            if recvd[3] == 'BULLET' and recvd[4] == 'ENEMY':
                for i in clients:
                    i.send(pickle.dumps(['DIE',recvd[2]]))
            elif recvd[3] == 'PLAYER' and recvd[4] == 'ENEMY':
                for i in clients:
                    i.send(pickle.dumps(['COMMIT TAKE HEALTH',recvd[2],recvd[0]])
        
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
