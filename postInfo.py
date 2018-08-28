import tweepy
from datetime import datetime, date, timedelta
import sys
sys.path.insert(0, '/home/pi/repositories/configs/')
import configSettings_ppe as configSettings

def postInfo(val, type, id):
    api=configSettings.get_api()
    tweet = "the value is: "+str(val)+" #"+str(type)+" #"+str(id)+" at:"+str(datetime.now()) # add time to avoid repeated tweets
    info = api.update_status(status=tweet)
    # Yes, tweet is called 'status' rather confusing
    return info

