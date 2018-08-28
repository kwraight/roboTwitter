import tweepy
from datetime import datetime, date, timedelta
import sys
import argumentClass
sys.path.insert(0, '../configs/')
import configSettings_ppe as configSettings

def postInfo(val, type, id):
    api=configSettings.get_api()
    for i in range(0,5,1):
        tweet = "the value is: "+str(val)+" #"+str(type)+" #"+str(id)+" at:"+str(datetime.now()) # add time to avoid repeated tweets
        status = api.update_status(status=tweet)
# Yes, tweet is called 'status' rather confusing


def main():

    print ">>>postInfo running..."

    ### get the inputs
    args = argumentClass.PostArgs()
    #print args

    postDict={}
    ### set parameters
    for k in vars(args).iteritems():
        postDict[k[0]]=k[1]
        
    print postDict

    postInfo(postDict['value'], postDict['type'], postDict['id'])

    print ">>>postInfo running..."


if __name__ == "__main__":
    main()

    #some values to post
