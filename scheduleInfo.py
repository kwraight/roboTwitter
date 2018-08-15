#basic schedule test
import schedule
import subprocess
import time

def job():
    print "I'm working"

def jobFile():
    print subprocess.check_output(['python','/afs/phas.gla.ac.uk/user/k/kwraight/testJob.py'])

schedule.every(1).minutes.do(jobFile)
schedule.every(0.75).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
