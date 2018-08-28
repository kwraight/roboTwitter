""" 
dht22.py 
Temperature/Humidity monitor using Raspberry Pi and DHT22. 
Data is displayed at thingspeak.com
Original author: Mahesh Venkitachalam at electronut.in 
Modified by Adam Garbo on December 1, 2016 
""" 
import sys 
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep 
import Adafruit_DHT 
import urllib2
sys.path.insert(0, '/home/pi/repositories/configs/')
import configSettings_ppe as configSettings

GPIO_PIN=19


def tweetInfo(infotxt, type, id):
    api=configSettings.get_api()
    tweet = str(infotxt)+" #"+str(type)+" #"+str(id)+" at: "+str(datetime.now()) # add time to avoid repeated tweets
    info = api.update_status(status=tweet)
    # Yes, tweet is called 'status' rather confusing
    return info

def getSensorData(): 
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, GPIO_PIN) 
   return (str(RH), str(T)) 
def main(): 
   print 'starting...' 
   while True:
       RH, T = getSensorData() 
       infotxt= "test from afar T/H(C/%): {0} / {1}".format(T,RH)
       print infotxt
       tweetInfo(infotxt,"tempHum","RoboPi")
       sleep(300) #loads DHT22 sensor values every 5 minutes
       
# call main 
if __name__ == '__main__': 
   main()
   
