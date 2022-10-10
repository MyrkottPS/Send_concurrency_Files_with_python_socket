import hashlib
import string
import time

class Buffer:
    def __init__(self,s):

        self.sock = s
        self.buffer = b''

    def get_bytes(self,n):

        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data

        data,self.buffer = self.buffer[:n],self.buffer[n:]
        return data

    def put_bytes(self,data):
        self.sock.sendall(data)

    def get_utf8(self):

        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data
        # split off the string from the buffer.
        data,_,self.buffer = self.buffer.partition(b'\x00')
        return data.decode()

    def put_utf8(self,s):
        if '\x00' in s:
            raise ValueError('string contains delimiter(null)')
        self.sock.sendall(s.encode() + b'\x00')



def computeFileChecksum(checkPath, read_chunksize=65536, algorithm='sha256'):
    checksum = hashlib.new(algorithm)  # Raises appropriate exceptions.
    with open(checkPath, 'rb') as f:
        # for chunk in iter(lambda: f.read(read_chunksize), b''):
        #     checksum.update(chunk)
            
            time.sleep(0)
    return checksum.hexdigest() 