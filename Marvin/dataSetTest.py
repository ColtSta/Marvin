import io
import picamera
import cv2
import numpy
import sys
import sqlite3
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (500, 350)

def insertOrUpdate(Id, Name):
	conn = sqlite3.connect("facialRecognition.db")
	cmd = "SELECT id,Name FROM People WHERE id =" +str(Id)
	cursor = conn.execute(cmd)
	isRecordExist = 0
	for row in cursor:
		isRecordExist = 1
	if(isRecordExist == 1):
		cmd = "UPDATE People SET Name ="+str(Name)+" WHERE id = "+str(Id)
	else:
		cmd = "INSERT INTO People(id, Name) values("+str(Id)+", "+str(Name)+")"
	conn.execute(cmd)
	conn.commit()
	conn.close()
 
sys.path.append('/usr/local/lib/python2.7/site-packages')
#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

id = raw_input("Enter user ID: ")
userName = raw_input("Enter user name: ")
sampleNum = 0
insertOrUpdate(id, userName)

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
while 1:
	stream = io.BytesIO()
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

#Draw a rectangle around every found face
	for (x,y,w,h) in faces:
    		sampleNum = sampleNum + 1
    		cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    	cv2.imwrite("dataSet/" + str(userName) + "." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
#    	cv2.waitKey(1)
	stream.close()
	print sampleNum
	if (sampleNum > 149):
		break
#Save the result image
#cv2.imwrite('result.jpg',image)
