import tweepy
from datetime import datetime, date, timedelta
sys.path.insert(0, '../configs/')
import configSettings_ppe

def postInfo(val, type, id):
    api=configSettings.get_api()
    for i in range(0,5,1):
        tweet = "the value is: "+str(val)+" #"+str(type)+" #"+str(id)+" at:"+str(datetime.now()) # add time to avoid repeated tweets
        status = api.update_status(status=tweet)
# Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
    main()

    #some values to post
