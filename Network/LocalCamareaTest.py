import cv2
import threading
import time
import numpy as np

class Mode():
    DEBUG = 1
    TESTING = 2
class Color():
    PRIMARY = (255, 255, 0)
    SECONDARY = (230, 230, 15)
    ACCENT = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
class Font:
    FACE = cv2.FONT_HERSHEY_SIMPLEX
    SCALE = .75
    COLOR = Color.WHITE
    LINE = 2

    def renderText(x, y, frame, text):
        cv2.putText(frame, text,
            (x, y), 
            Font.FACE, 
            Font.SCALE,
            Font.COLOR,
            Font.LINE)
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def checkIntersection(self, x, y, width, height):
        if (x >= self.x and
            x <= self.x + (self.width) and
            y >= self.y and y
            <= self.y + (self.height)):
            return True
class StreamVideo:

    def __init__(self, source):
        self.video = None
        self.videoContainer = []
        self.windowLoaded = False
        self.loadingVideoPrimary = False
        self.mode = False
        self.detectMotion = False
        self.appName = 'Baby Stuff'
        self.static_back = None
        self.clickedCoordinates = []
        self.boundingRectangle = None
        self.width = 1280
        self.height = 720
        self.threshValue = 8
    def loadVideo(self):
        if self.loadingVideoPrimary == False:
            self.loadingVideoPrimary = True
            print('loading video source primary')
            self.video = cv2.VideoCapture(0)
            self.video.set(3, self.width)
            self.video.set(4, self.height)
            time.sleep(0)
        else:
            print('loading video source secondary')
            self.videoContainer.append(cv2.VideoCapture(1))
            self.videoContainer[0].set(3, self.width)
            self.videoContainer[0].set(4, self.height)

    def draw_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            if (len(self.clickedCoordinates) < 2):
                self.clickedCoordinates.append((x,y))
                if len(self.clickedCoordinates) == 1:
                    self.static_back = None
                if len(self.clickedCoordinates) == 2:
                    self.boundingRectangle = Rectangle(
                        self.clickedCoordinates[0][0],
                        self.clickedCoordinates[0][1],
                        self.clickedCoordinates[0][0] + (self.clickedCoordinates[1][0] - self.clickedCoordinates[0][0]),
                        self.clickedCoordinates[0][1] + (self.clickedCoordinates[1][1] - self.clickedCoordinates[0][1]))

            else:
                del self.clickedCoordinates[:]
                self.boundingRectangle = None
        
                
    def findMotion(self, frame):
        gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (1, 1), 0) 
        if np.shape(self.static_back) != ():
            thresh_frame = cv2.dilate(
                (cv2.threshold(
                cv2.absdiff(self.static_back, gray),
                self.threshValue,
                255,
                cv2.THRESH_BINARY)[1]),
                None,
                iterations = 1)
            if self.mode == True:
                return thresh_frame
            (allContours, v1) = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if self.boundingRectangle != None:
                for contour in allContours:
                    if cv2.contourArea(contour) < 4000: 
                        continue  
                    (x, y, w, h) = cv2.boundingRect(contour)
                    if self.boundingRectangle.checkIntersection(x, y, w, h):
                        cv2.rectangle(frame, (x, y), (x + w, y + h), Color.ACCENT, 2)
                        Font.renderText(x, y, frame, str(x) + ' ' + str(y))
            return frame
        else:
            self.static_back = gray
            return frame
    def handleInput(self, key):
        if key == ord('q'): 
            print('closing ' + self.appName)
            self.video.release()
            self.videoContainer[0].release()
            cv2.destroyAllWindows()
            return False
        if key == ord('w'):
            self.static_back = None
            print('reset static back')
        if key == ord('1'):
            if self.videoContainer[0] != None:
                if self.videoContainer[0].isOpened():
                    self.videoContainer.append(self.video)
                    self.video = self.videoContainer.pop(0)
        if key == ord('2'):
            if self.detectMotion == False:
                self.detectMotion = True
            else:
                self.detectMotion = False
        if key == ord('3'):
            if self.mode == False:
                self.mode = True
            else:
                self.mode = False
        if key == ord('p'):
            print('Mode: ' + str(self.mode))
            print('Motion Detection: ' + str(self.detectMotion))
    def playVideoSource(self):
        while True:
            if self.video != None:
                if self.video.isOpened():
                    check, frame = self.video.read()
                    if np.shape(frame) == ():
                        continue
                    if self.detectMotion == True:
                        frame = self.findMotion(frame)
                    if len(self.clickedCoordinates) == 1:
                        cv2.circle(frame, self.clickedCoordinates[0], 5, Color.SECONDARY,-1)
                    elif len(self.clickedCoordinates) == 2:
                        cords1 = self.clickedCoordinates[0]
                        cords2 = self.clickedCoordinates[1]
                        cv2.rectangle(frame, cords1, (cords1[0] + (cords2[0] - cords1[0]), cords1[1] + (cords2[1] - cords1[1])), Color.PRIMARY, 1)
                    #Render final frame
                    cv2.imshow(self.appName, frame)
     
                    key = cv2.waitKey(1)
                    inValue = self.handleInput(key)
                    if inValue == False:
                        break;
                    
            else:
                if self.windowLoaded == False:
                    if self.video != None:
                        self.video.set(3, self.width)
                        self.video.set(4, self.height)
                    cv2.namedWindow(self.appName, cv2.WINDOW_NORMAL)
                    cv2.resizeWindow(self.appName, self.width, self.height)
                    cv2.moveWindow(self.appName, 500, 500)
                    cv2.setMouseCallback(self.appName, self.draw_circle)
                    self.windowLoaded = True
                    print('Window loaded..')
                print('Loading...')                
                time.sleep(5)
    def run(self):
        t1 = threading.Thread(target=self.loadVideo)
        t2 = threading.Thread(target=self.loadVideo)
        t3 = threading.Thread(target=self.playVideoSource)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
 
vidStream = StreamVideo(1)
vidStream.run()
