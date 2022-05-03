# import the necessary packages
from threading import Thread
import cv2, time
import math

class WebcamVideoStream:
    def __init__(self, src=0, FPS=5, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
        self.stream.set(cv2.CAP_PROP_FPS,FPS)
        #self.stream.set(cv2.CAP_PROP_BRIGHTNESS, int(2))
        self.crop_img = []
        (self.grabbed, self.frame) = self.stream.read()


        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
        # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                break
        # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        if self.grabbed:
            self.crop_img = self.frame.copy()
            #self.crop_img = self.crop_img[self.cutted-100:self.cutted+1004,578:1874] #144:880,528:1392 (864,736)
            #print("W:%s, H:%s"%(self.frame.shape[0],self.frame.shape[1])) 
            #self.crop_img = cv2.resize(self.crop_img, (1920, 1080))
            #crop_img = cv2.resize(crop_img, self.resize)
        else:
            return self.grabbed, None
        return self.grabbed, self.crop_img

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
