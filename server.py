import socket  
  
address = ('0.0.0.0', 8887)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
s.bind(address)  
s.listen(5)  



ss, addr = s.accept()  
print('got connected from',addr)
while(True):
    ra = ss.recv(4096)  
    # print(ra)
    if ra != b'':
        print(ra)
    else:
        break
  
ss.close()  
s.close()  