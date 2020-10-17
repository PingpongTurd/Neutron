import socket
import time
import pickle
import random

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.100'
port = 8888
client.connect((host,port))
client.send(pickle.dumps([0,"td"]))
while True: 
    a= pickle.loads(client.recv(1024))
    print(a)
    break
