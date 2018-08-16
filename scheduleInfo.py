#basic schedule test
import schedule
import subprocess
import time
import datetime

#def job():
#    print "I'm working"

def job():
    print subprocess.check_output(['python', '/home/pi/repositories/roboTwitter/summaryInfo.py', '--robos', '8266', 'Uno', '--type', 'temp', '--arguments', '4'])
    print "done job for today:\n",datetime.datetime.now()

schedule.every(24).hours.do(jobFile)
schedule.every(0.75).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
