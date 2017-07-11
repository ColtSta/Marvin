# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import sys
import os
import sqlite3

def getProfile(id):
        conn = sqlite3.connect("/home/pi/Projects/Marvin/facialRecognition.db")
        cmd = "SELECT * FROM People WHERE id = "+str(id)
        cursor = conn.execute(cmd)
        profile = None
        for row in cursor:
                profile = row
        conn.close()
        return profile

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('/home/pi/Projects/Marvin/recognizer/trainingData.yml')
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
#camera.resolution = (640, 480)
camera.resolution = (800, 500)
camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))
rawCapture = PiRGBArray(camera, size = (800, 500))

# allow the camera to warmup
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('/home/pi/Projects/RaspiCam/marvins_eye/faces.xml')
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)


	for (x,y,w,h) in faces:
	        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),1)
		Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        	profile = getProfile(Id)

        	if(conf < 38):
                	if(profile != None):
                        	cv2.cv.PutText(cv2.cv.fromarray(image), str(profile[1]), (x,y+h+30),font,255)
				cv2.cv.PutText(cv2.cv.fromarray(image), str("%.2f" % conf), (x,y+h+60),font,255)
				cv2.cv.PutText(cv2.cv.fromarray(image), str(Id), (x, y+h+90), font, 255)

               		else:
                	        cv2.cv.PutText(cv2.cv.fromarray(image), str("Unknown"), (x,y+h+30), font, 255)
        	else:
                	cv2.cv.PutText(cv2.cv.fromarray(image), str("Unknown"), (x, y+h+30), font, 255)

 
	# show the frame
	cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN) 
	cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
