import tweepy
from datetime import datetime, date, time
import time
import ../configSettings_ppe
    
    api=configSettings.get_api()
    for i in range(0,5,1):
        tweet = "the time is: "+str(datetime.now())+" #thisAction #thisGuy"
        if "NYS" not in tweet:
            print "tweet:",tweet
            status = api.update_status(status=tweet)
            time.sleep(10)
# Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
    main()

