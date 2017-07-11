#!/usr/bin/env python

import io
import picamera
import cv2
import numpy
import sys

#sys.path.append('/usr/local/lib/python2.7/site-packages')
#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
with picamera.PiCamera() as camera:
    camera.resolution = (500, 350)
    camera.brightness = (50)
    camera.capture(stream, format='jpeg')

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

#print "Found "+str(len(faces))+" face(s)"
print str(len(faces))
#Draw a rectangle around every found face
for (x,y,w,h) in faces:
	cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
#Save the result image
cv2.imwrite('result.jpg',image)
