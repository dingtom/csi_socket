import socket
import struct
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy import signal

from read_bf_file import read_bfee

class UpdateFig(object):
    def __init__(self, ax, ss, init_length, step_length, fs, low_pass_freq, low_stop_freq, low_Rp, low_Rs, high_pass_freq, high_stop_freq, high_Rp, high_Rs):
        self.ax = ax
        self.line, = ax.plot([], [])
        self.ax.set_xlim(0, step_length)
        self.ax.set_ylim(-50, 200)

        self.ss = ss
        self.fs = fs
        self.low_pass_freq = low_pass_freq
        self.low_stop_freq = low_stop_freq
        self.low_Rp = low_Rp
        self.low_Rs = low_Rs
        self.high_pass_freq = high_pass_freq
        self.high_stop_freq = high_stop_freq
        self.high_Rp = high_Rp
        self.high_Rs = high_Rs
        self.init_length = init_length
        self.step_length = step_length
        self.t = np.linspace(0, init_length, init_length, endpoint=True)
        self.csi_list = []
        pass
    
    def init(self):
        count = 0
        while count < self.init_length:
            ra = self.ss.recv(4096)
            if ra != b'':
                if ra[0] == 187:
                    csi = read_bfee(ra[1:])
                    self.csi_list.append(csi.csi)
                    count += 1
            else:
                break
        csi_np_array = np.array(self.csi_list)
        print(csi_np_array.shape)        
        csi_stream = np.absolute(csi_np_array[:,:,0,0])
        data = csi_stream.transpose(1,0)
        # print(csi_stream.shape)
        data = self.butter_lowpass(data, self.low_pass_freq, self.low_stop_freq, self.low_Rp, self.low_Rs)
        data = self.butter_highpass(data, self.high_pass_freq, self.high_stop_freq, self.high_Rp, self.high_Rs)
        self.line.set_data(self.t, data[1,:])
        return self.line,

    def __call__(self, i):
        if i == 0:
            return self.init()
        count = 0
        self.csi_list = self.csi_list[self.step_length:]
        while count < self.step_length:
            ra = self.ss.recv(4096)
            if ra != b'':
                if ra[0] == 187:
                    csi = read_bfee(ra[1:])
                    self.csi_list.append(csi.csi)
                    count += 1
            else:
                break
        csi_np_array = np.array(self.csi_list)        
        print(csi_np_array.shape)
        csi_stream = np.absolute(csi_np_array[:,:,0,0])
        data = csi_stream.transpose(1,0)
        # print(csi_stream.shape)
        data = self.butter_lowpass(data, self.low_pass_freq, self.low_stop_freq, self.low_Rp, self.low_Rs)
        data = self.butter_highpass(data, self.high_pass_freq, self.high_stop_freq, self.high_Rp, self.high_Rs)
        self.line.set_data(self.t, data[1,:])
        return self.line,

    def butter_lowpass(self, data, pass_freq, stop_freq, Rp = 3, Rs = 30, fs = 1000):
        Wp = pass_freq / (fs / 2)
        Ws = stop_freq / (fs / 2)

        N, Wn = signal.buttord(Wp, Ws, Rp, Rs)
        b, a = signal.butter(N, Wn, 'low')
        y = signal.lfilter(b, a, data)
        return y

    def butter_highpass(self, data, pass_freq, stop_freq, Rp = 0.5, Rs = 40, fs = 1000):
        Wp = pass_freq / (fs / 2)
        Ws = stop_freq / (fs / 2)

        N, Wn = signal.buttord(Wp, Ws, Rp, Rs)
        b, a = signal.butter(N, Wn, 'high')
        y = signal.lfilter(b, a, data)
        return y
def main():
    fs = 1000.0
    low_pass_freq = 80
    low_stop_freq = 95
    low_Rp = 3
    low_Rs = 30

    high_pass_freq = 10
    high_stop_freq = 5
    high_Rp = 0.5
    high_Rs = 40
    
    
    address = ('0.0.0.0', 8887)  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
    s.bind(address)  
    s.listen(1)
    ss, addr = s.accept()  
    print('got connected from',addr)

    init_length = 4000
    step_length = 1000
    
    fig, ax = plt.subplots()
    uf = UpdateFig(ax, ss, init_length, step_length, fs, low_pass_freq, low_stop_freq, low_Rp, low_Rs, high_pass_freq, high_stop_freq, high_Rp, high_Rs)

    anim = FuncAnimation(fig, uf, init_func=uf.init, interval=1000, blit=True, save_count=50)
    plt.show()

    ss.close()  
    s.close()  

if __name__ == '__main__':
    main()
