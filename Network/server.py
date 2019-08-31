import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from random import randint
import threading

class CameraServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.connectionThreads = []

    def generateId(self):
        output = ""
        for i in range(0, 7):
            output += chr(randint(65, 90))
        return output
    def checkConnection(self):
        while True:
            print('checking connections...')
            connection, address = self.socket.accept()
            threadId = self.generateId()
            connection.send(threadId.encode())
            t1 = threading.Thread(target=self.getConnection, args=(connection, address, threadId))
            self.connectionThreads.append(t1)
            t1.start()
            
        
    def getConnection(self, conn, address, assignedId):
        data = b""
        payload_size = struct.calcsize(">L")
        print("Connected to client at ", address)
        while True:

            while len(data) < payload_size:
                data += conn.recv(512)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(512)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('test' ,frame)
            key = cv2.waitKey(1)
            
    def run(self):
        t0 = threading.Thread(target=self.checkConnection)
        t0.start()
        t0.join()
        
if __name__ == "__main__":
    cameraServer = CameraServer('192.168.0.5', 12345)
    cameraServer.run()
