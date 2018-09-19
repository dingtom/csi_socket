import socket
import struct
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from read_bf_file import read_bfee

def butter_lowpass(data, pass_freq, stop_freq, Rp = 3, Rs = 30, fs = 1000):
    Wp = pass_freq / (fs / 2)
    Ws = stop_freq / (fs / 2)

    N, Wn = signal.buttord(Wp, Ws, Rp, Rs)
    b, a = signal.butter(N, Wn, 'low')
    y = signal.lfilter(b, a, data)
    return y

def butter_highpass(data, pass_freq, stop_freq, Rp = 0.5, Rs = 40, fs = 1000):
    Wp = pass_freq / (fs / 2)
    Ws = stop_freq / (fs / 2)

    N, Wn = signal.buttord(Wp, Ws, Rp, Rs)
    b, a = signal.butter(N, Wn, 'high')
    y = signal.lfilter(b, a, data)
    return y

def plot_signal(data, fs, low_pass_freq, low_stop_freq, low_Rp, low_Rs,
                high_pass_freq, high_stop_freq, high_Rp, high_Rs,t):
        plt.figure()
        # plt.ion()
        plt.clf()
        plt.plot(t, data[1,:], label='Noisy signal')
        data = butter_lowpass(data, low_pass_freq, low_stop_freq, low_Rp, low_Rs)
        data = butter_highpass(data, high_pass_freq, high_stop_freq, high_Rp, high_Rs)
        print(data.shape)
        plt.plot(t, data[1,:], label='Filtered signal')
        # w, h = signal.freqs(b, a, np.linspace(0,500,1000))
        # plt.plot(w, 20 * np.log10(abs(h)))
        plt.show()

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

    count = 0
    step_length = 4000
    csi_list = []
    t = np.linspace(0, step_length, step_length, endpoint=True)
    
    start_time = time.time()
    while(True):
        ra = ss.recv(4096)  
        # print(ra)
        if ra != b'':
            if ra[0] == 187:
                csi = read_bfee(ra[1:])
                csi_list.append(csi.csi)
                count += 1
        else:
            break
        if count == step_length:
            end_time = time.time()
            print(step_length / (end_time - start_time))
            start_time = time.time()
            count = 0
            csi_np_array = np.array(csi_list)
            csi_list = []
            csi_stream = np.absolute(csi_np_array[:,:,0,0])
            csi_stream = csi_stream.transpose(1,0)
            print(csi_stream.shape)
            #plot_signal(b, a, csi_np_array)
            plot_signal(csi_stream, fs, low_pass_freq, low_stop_freq, low_Rp, low_Rs,
                    high_pass_freq, high_stop_freq, high_Rp, high_Rs,t)
            print("plot finish")
            #break
    ss.close()  
    s.close()  

if __name__ == '__main__':
    main()