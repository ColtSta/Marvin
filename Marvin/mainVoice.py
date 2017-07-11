
import RPi.GPIO as GPIO
import time
import os
import speech_recognition
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
#Start listening for a command and write what is heard to a txt file.
os.system("speech-recog.sh > stt.txt")

#Read in the text file to the 'speech' variable
with open ("stt.txt", "r") as myFile:
	speech = myFile.readlines()

#Case check and respond with espeak. Each response is read from a txt file
if(speech == ['"hello Marvin"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 good,evening 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
	GPIO.cleanup()

elif(speech == ['"I Love You Marvin"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 -f responses/loveResponse.txt 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()

elif(speech == ['"start the Stream"']):
	os.system("python Test/faceTestv2.py")

elif(speech == ['"who are you"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 My,name,is,Marvin...I,am,the,creation,of,the,geniuses,you,see,before,you 2>/dev/null")
	os.system("espeak -ven -s130 I,am,capable,of,counting,and,identifying,people,that,I,see 2>/dev/null")
	os.system("espeak -ven -s130 I,am,also,at,a,rough,estimate,30,billion,times,more,intelligent,than,you 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
	GPIO.cleanup()

elif(speech == ['"how are you doing"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 well...it,is,another,great,day,at,BYU-Idaho 2>/dev/null")
	os.system("espeak -ven -s130 so,obviously,I,am,doing,fantastic 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
	GPIO.cleanup()

elif(speech == ['"who do you recognize"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 -f responses/letMeSee.txt 2>/dev/null")
	GPIO.output(17, GPIO.LOW)

	os.system("python detectorTest.py > responses/recognized.txt")
	GPIO.output(17, GPIO.HIGH)
	#os.system("espeak -ven -s130 -f responses/myFriend.txt 2>/dev/null")
	os.system("espeak -ven -s130 -f responses/recognized.txt 2>/dev/null")
	#os.system("espeak -ven -s130 -f responses/isInTheRoom.txt 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()

elif(speech == ['"who\'s your favorite"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 my,creators,Sean,Colten,Jared,and,Leo,are,my,favorites 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
	GPIO.cleanup()

elif(speech == ['"how many people are in the room"']):
	os.system("python peopleCounting.py > responses/peopleCount.txt")
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 -f responses/thereAre.txt 2>/dev/null")
	os.system("espeak -ven -s130 -f responses/peopleCount.txt 2>/dev/null")
	os.system("espeak -ven -s130 -f responses/peopleInTheRoom.txt 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()
elif(speech == ['"who is Brooklyn"']):
	os.system("espeak -ven -s130 the,most,beautiful,girl,in,the,world 2>/dev/null")

elif(speech == ['"what\'s the weather like in Rexburg Idaho"']):
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -s130 there,are,most,likely,gusts,of,wind,over,20,miles,per,hour 2>/dev/null")
	os.system("espeak -ven -s130 and,its,either,freezing,cold,or,unbearably,hot 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
	GPIO.cleanup()
else:	
	GPIO.output(17, GPIO.HIGH)
	os.system("espeak -ven -f responses/unknownCommand.txt 2>/dev/null")
	GPIO.output(17, GPIO.LOW)
        GPIO.cleanup()

print speech
	#os.system("espeak -ven -s130 -f peopleCount.txt 2>/dev/null")		

#if(text == "hello Marvin"):
#	os.system("espeak -ven -s130 -f wakeUP.txt 2>/dev/null")
#	counter = counter + 1
#	print counter
