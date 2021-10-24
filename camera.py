#!/usr/bin/python3
import face_recognition
import cv2
import os
import pickle
import time

class Camera(object):
    def __init__(self):
        print(cv2.__version__)
        global fpsReport
        global scaleFactor
        global Names
        global knownFaces
        global font
        fpsReport=0
        scaleFactor=1
        dispW=640
        dispH=480

        knownFaces=[]
        Names=[]

        with open('/tmp/train.pkl','rb') as f:
            Names=pickle.load(f)
            knownFaces=pickle.load(f)

        font=cv2.FONT_HERSHEY_SIMPLEX
        self.video=cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 30)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

    def get_frame(self):
        global fpsReport
        timeStamp=time.time()
        _,frame=self.video.read()
        #frame=cv2.resize(frame,(640,360))
        frameSmall=cv2.resize(frame,(0,0),fx=scaleFactor,fy=scaleFactor)
        frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
        facePositions=face_recognition.face_locations(frameRGB,model='cnn')
        allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
        for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings):
            name='Unknown Person'
            matches=face_recognition.compare_faces(knownFaces,face_encoding)
            if True in matches:
                first_match_index=matches.index(True)
                name=Names[first_match_index]
            top=int(top/scaleFactor)
            right=int(right/scaleFactor)
            bottom=int(bottom/scaleFactor)
            left=int(left/scaleFactor)
            cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
            cv2.putText(frame,name,(left,top-6),font,.75,(255,255,0),2)
        dt=time.time()-timeStamp
        fps=1/dt
        fpsReport=.90*fpsReport+.1*fps
        cv2.putText(frame,str(round(fpsReport,1))+'fps',(0,25),font,.75,(255,0,0,2))
        #print('fps is:',fps)
        #cv2.imshow('Picture',frame)
        #cv2.moveWindow('Picture',0,0)
        _,frame=cv2.imencode('.jpg',frame)
        return frame

    def __del__(self):
            self.video.release()

