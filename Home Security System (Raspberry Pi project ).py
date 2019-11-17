import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from smtplib import SMTPException

camera = PiCamera()
date_string = time.strftime("%Y-%m-%d_%H.%M.%S") #Adds date and time to the image
f_time = datetime.now().strftime('%a %d %b @ %H:%M')#Adds date and time to the video

#EMAIL Login
smtpUser = 'example@gmail.com'
smtpPass= 'password'

#To address 
toaddr='example@gmail.com'
me = 'example@gmail.com' 
fromAdd= smtpUser

#GPIO SENSOR
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensorwhile True:
while True:
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i

#CAMERA
        camera.capture(date_string+".jpg")
        recording = datetime.now().strftime(date_string+".h264")
        camera.start_recording(recording)
        camera.start_preview()
        sleep(5)
        camera.stop_recording()
        camera.stop_preview()
        
 
        subject = 'This Photo was taken @ ' + f_time
#        header = 'to:' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject


#ALERT EMAIL
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        msg.preamble = "This Photo was taken @ " + f_time
        body='Motion was detected on your security Camera.'
        msg['Body'] = body
 
        print subject + '\n' + body
        fp = open(date_string+".jpg", 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        try:
           s = smtplib.SMTP('smtp.gmail.com',587)
           s.ehlo()
           s.starttls()
           s.ehlo()
           s.login(user = 'example@gmail.com',password = 'password')
           #s.send_message(msg)
           s.sendmail(me, toaddr, msg.as_string())
           s.quit()

        #except:
        #   print ("Error: unable to send email")
        except SMTPException as error:
              print "Error: unable to send email :  {err}".format(err=error)
        
        time.sleep(0.1)
