import socket
import struct
from read_bf_file import read_bfee

address = ('0.0.0.0', 8887)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
s.bind(address)  
s.listen(5)  



ss, addr = s.accept()  
print('got connected from',addr)
while(True):
    ra = ss.recv(8192)  
    # print(ra)
    if ra != b'':
        if ra[0] == 187:
            csi = read_bfee(ra[1:])
            print(csi.timestamp_low)
    else:
        break
  
ss.close()  
s.close()  