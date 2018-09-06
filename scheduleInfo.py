#basic schedule job to use summaryInfo to summarise data, delete data and tweet summary plot
import schedule
import subprocess
import time
import datetime

#def job():
#    print "I'm working"

def job():
    jobArgs=['python', '/home/pi/repositories/roboTwitter/summaryInfo.py', '--robos', '8266', 'Uno', 'Pi', '--type', 'temp', '--deleteOpt', 'True', '--arguments', '4']
    print " ".join(jobArgs)
    print subprocess.check_output(jobArgs)
    print "done job for today:\n",datetime.datetime.now()

schedule.every().day.at("20:40").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
