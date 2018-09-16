import socket

address = ('127.0.0.1',8887)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(address)
while(True):
    s.send(b"hh")
s.close()