import socket
import cv2
import numpy
import pickle
import struct
import threading
import time
import sys
import enum

class CameraProbe:
    def __init__(self, host, port, cameraId):
        self.connectionString = (host, port)
        self.cameraId = cameraId
        self.socket = socket.socket()
        self.encodeParameter = [int(cv2.IMWRITE_JPEG_QUALITY),90]
        self.camera = None
        self.connected = False
        self.errorFlag = False
        self.assignedId = None
    def connectToServer(self):
        print(' Connecting to server: ' + str(self.connectionString) + '\n\r')
        time.sleep(0)
        try:
            self.socket.connect(self.connectionString)
            self.connected = True
        except socket.error as e:
            self.shutdown(e)
    def initializeCamera(self):
        print('Initializing Camera...\n\r')
        time.sleep(0)
        self.camera = cv2.VideoCapture(self.cameraId)
    def communicateWithServer(self):
        print('Trying to communicate with server \n\r')
        time.sleep(0)
        while self.errorFlag == False:
            if self.camera != None:
                if self.camera.isOpened() == False:
                    continue
                ret, frame = self.camera.read()
                if numpy.shape(frame) == ():
                    continue
                result, imgencode = cv2.imencode('.jpg', frame, self.encodeParameter)
                data = pickle.dumps(imgencode, 0)
                size = len(data)
                if self.connected == True:
                    try:
                        if self.assignedId == None:
                            self.assignedId = self.socket.recv(8).decode()
                            print('assigned ID: ' + self.assignedId)
                        self.socket.send(struct.pack(">L", size) + data)
                    except socket.error as e:
                        self.shutdown(e)
        self.shutdown('Loop Broken')

    def shutdown(self, error):
        print(error)
        self.errorFlag = True
        self.connected = False
        if self.camera != None:
            self.camera.release()
        self.socket.close()
        sys.exit(0)
    def tryReconnect(self):
        print('Trying to reconnecto to server: ' + self.connectionString)
    def run(self):
        t0 = threading.Thread(target=self.connectToServer)
        t1 = threading.Thread(target=self.initializeCamera)
        t2 = threading.Thread(target=self.communicateWithServer)
        t0.start()
        t1.start()
        t2.start()
        t0.join()
        t1.join()
        t2.join()

if __name__ == '__main__':
    probe = CameraProbe('192.168.0.5', 12345, 0)
    probe.run()

