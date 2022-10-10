import socket
import time
import os
import sys
import Buffer
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import hashlib
import time



HOST = '127.0.0.1'
PORT = 4040

def socketVar():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return s

def sendFile(filename):
        s = socketVar()
        sbuf = Buffer.Buffer(s)
        s.connect((HOST, PORT))

        sbuf.put_utf8(filename)
        
        fileSize = os.path.getsize(filename)
        sbuf.put_utf8(str(fileSize))
        checkSum = Buffer.computeFileChecksum(filename)
        sbuf.put_utf8(checkSum)
        with open(filename, 'rb') as f:
            sbuf.put_bytes(f.read())




def main():

    if len(sys.argv) > 1:   
        folderPath = sys.argv[1]
        path = rf'{folderPath}'
        readFolder = os.listdir(str(path))
        os.chdir(str(path))
        if len(sys.argv) == 3:
            numConcurrency = int(sys.argv[2])
            with Pool(numConcurrency) as p:
                t1 = time.time()
                for i in range(0,len(readFolder), numConcurrency):
                    
                    p.map(sendFile, readFolder[i:i+numConcurrency])
                t2 = time.time()
                throughput = round((10240*1000 * 0.001) / (t2 - t1), 3) 

        elif len(sys.argv) == 2:
            t3 = time.time()
            for i in readFolder:
                sendFile(i)
            t4 = time.time()
            throughput = round((os.path.getsize(i) * 0.001) / (t4 - t3), 3)
    else:
        print("Input Arguments must be: python Client.py [Folder name] [Number of concurrency files]")
    return print(throughput)
    


if __name__ == '__main__':
       main()


