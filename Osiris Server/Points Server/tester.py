import socket
import time
import pickle
import random

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'edi.geinc.xyz'
port = 80
client.connect((host,port))
nm = input("> ")
sc = input("> ")
client.send(pickle.dumps([nm,sc]))
