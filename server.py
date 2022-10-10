import socket
import os

import Buffer

HOST = ''
PORT = 4040

try:
    os.mkdir('uploads')
except FileExistsError:
    pass

s = socket.socket()
s.bind((HOST, PORT))
s.listen(10)
print("Waiting for a connection.....")

while True:
    conn, addr = s.accept()
    print("Got a connection from ", addr)
    connbuf = Buffer.Buffer(conn)

    while True:
        fileName = connbuf.get_utf8()
        if not fileName:
            break
        fileName = os.path.join('uploads',fileName)
        print('file name: ', fileName)

        fileSize = int(connbuf.get_utf8())
        print('file size: ', fileSize )

        checkSum = connbuf.get_utf8()

        

        with open(fileName, 'wb') as f:
            remaining = fileSize
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = connbuf.get_bytes(chunk_size)
                if not chunk: break
                f.write(chunk)
                remaining -= len(chunk)
            if remaining:
                print('File incomplete.  Missing',remaining,'bytes.')
            else:
                getCheckSum = Buffer.computeFileChecksum(fileName)
                if str(getCheckSum) == checkSum:
                    print('File received successfully.')
                else:
                    print("Something wrong in file checksum")
    print('Connection closed.')
    conn.close()
                