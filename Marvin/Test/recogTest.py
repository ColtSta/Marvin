#import dataSetTest
#import trainerTest
import io
import picamera
import cv2
import numpy
import sys
import os
import sqlite3
import RPi.GPIO as GPIO
import time
import speech_recognition
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)


def getProfile(id):
	conn = sqlite3.connect("/home/pi/Projects/Marvin/facialRecognition.db")
	cmd = "SELECT * FROM People WHERE id = "+str(id)
	cursor = conn.execute(cmd)
	profile = None
	for row in cursor:
		profile = row
	conn.close()
	return profile


sys.path.append('/usr/local/lib/python2.7/site-packages')

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('/home/pi/Projects/Marvin/recognizer/trainingData.yml')
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 2, 2, 0, 2, 2)
#Create a memory stream so photos don't need to be saved in a file
stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
GPIO.output(17, GPIO.HIGH)
os.system("espeak -ven -s130 Say,cheese... 2>/dev/null")
GPIO.output(17, GPIO.LOW)
time.sleep(2)

with picamera.PiCamera() as camera:
	camera.resolution = (1000, 850)
	camera.capture(stream, format='jpeg')

GPIO.output(17, GPIO.HIGH)
os.system("espeak -ven -s130 -f responses/doneTakingPicture.txt 2>/dev/null")
GPIO.output(17, GPIO.LOW)

#Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
image = cv2.imdecode(buff, 1)

#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('/home/pi/Projects/RaspiCam/marvins_eye/faces.xml')

#Convert to grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

if(len(faces) == 0):
	os.system("espeak -ven -s130 I,am,sorry...I,cant,see,anyone 2>/dev/null")
	cv2.imwrite('result.jpg',image)
	sys.exit()

count = 0
Ids = []
Confs = []
Names = []

#Draw a rectangle around every found face
for (x,y,w,h) in faces:
	cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),1)
	#recognizer.load('recognizer/trainingData.yml')
	Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
	profile = getProfile(Id)
	Ids.append(Id)
	Confs.append(conf)
	Names.append(profile[1])

	if(conf < 36):
		if(profile != None):
			cv2.cv.PutText(cv2.cv.fromarray(image), str(profile[1]), (x,y+h+30),font,255)
		else:
			cv2.cv.PutText(cv2.cv.fromarray(image), str("Unknown"), (x,y+h+30), font, 255)
	else:
		cv2.cv.PutText(cv2.cv.fromarray(image), str("Unknown"), (x, y+h+30), font, 255)
#Save the result
nameLength = len(Names)
i = 0
if(nameLength > 1):
	print("my friends, ")
	while(i <= nameLength):
		if(Names[i] != "unknown"):
			print (Names[i] + ", ")
		i = i + 1
	print(" are in the room")
elif (Names != "unknown"):
	try:
		profile[1]
	except NameError:
		os.system("espeak -ven I,dont,see,anyone,I,recognize 2>/dev/null")
	else:		
		print("my friend, " + profile[1] + ", is in the room")

cv2.imwrite('result.jpg',image)
#print str(profile[1])
#print Names
#print Confs
