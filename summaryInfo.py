### use plotInfo to make plot from twitter info, save and post to twitter
import datetime
import os
import argparse
import tweepy

import plotInfo
import argumentClass
import sys
sys.path.insert(0, '../configs/')
import configSettings_ppe as configSettings


###############################
### USEFUL FUNCTIONS
###############################

def tweet_image(message, filename):
    api=configSettings.get_api()
    api.update_with_media(filename, status=message)
    #os.remove(filename)

###############################
### EXECUTE
###############################

def main():
    print ">>>summaryInfo running..."

    ### get the inputs
    args = argumentClass.GetArgs()
    print args

    ### basic dictionary of parameters
    sumDict={'noTweet':"False"}
    plotDict={'who':"FriendPpe", 'robos':["Uno","8266","Pi"], 'types':["temp"], 'start':"NYS", 'end':"NYS", 'groupOpt':"NYS", 'deleteOpt':"NYS", 'tweetArgs':[4], 'pages':-1, 'save':"False", 'saveName':"NYS"}
    sumDict.update(plotDict)

    ### set parameters
    for p in sumDict.keys():
        for k in vars(args).iteritems():
            if p in k[0] and not k[1]==None:
                print "got",k
                sumDict[p]=k[1]

    sumDict['start']=(datetime.datetime.now() - datetime.timedelta(1))
    sumDict['saveName']="summary_"+datetime.datetime.now().strftime("%Y-%m-%d")+".png"

    sumDict=plotInfo.FormatDict(sumDict)

    print "### summary dictionary\n",sumDict

    twitterInfo=plotInfo.GleanTwitter(sumDict)

    fileName=plotInfo.PlotData(sumDict,twitterInfo)

    if "False" in sumDict['noTweet'] or "false" in sumDict['noTweet']:
        message = "Summary for "+str(datetime.datetime.now().day)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().year)[2:]+" #summary"
        tweet_image(message, fileName)
    else:
        print "no update tweet sent as requested"
    print ">>>summaryInfo finished."

if __name__ == "__main__":
    main()
    exit()

