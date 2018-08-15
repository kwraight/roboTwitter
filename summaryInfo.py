
import datetime
import os
import subprocess
import argparse
import tweepy
import configSettings



def tweet_image(message, filename):
    api=configSettings.get_api()
    api.update_with_media(filename, status=message)
    #os.remove(filename)


parser = argparse.ArgumentParser()
parser.add_argument('--robos', nargs='+', help='name of robots')
parser.add_argument('--types', nargs='+', help='measurement type, e.g. temp')
parser.add_argument('--groupOpt', help='grouping for histogram: r - merge roboIDs; t - merge types; d split days')
parser.add_argument('--deleteOpt', help='delete used tweets')
parser.add_argument('--arguments', nargs='+', help='argument selection: which (space separated) (inetger) arguments from tweet (default=4,6)')
parser.add_argument('--noPlot', help='do not make plot for twitter update')

### check the inputs
args = parser.parse_args()
print args

### set parameters
roboIDs=[]
if not args.robos is None:
    roboIDs = args.robos

types=[]
if not args.types is None:
    types = args.types

if len(roboIDs)<1 or len(types)<1:
    print "please set robo and type arguments"
    exit()

tweetStrArgs=[]
if not args.arguments is None:
    tweetStrArgs=args.arguments
else:
    tweetStrArgs=[4]

noPlot="False"
if not args.noPlot is None:
    noPlot = args.noPlot

groupOpt="NYS"
if not args.groupOpt is None:
    groupOpt = args.groupOpt

deleteOpt="NYS"
if not args.deleteOpt is None:
    deleteOpt = args.deleteOpt

print ">>> summary parameters... \nroboIDs:",roboIDs,", types:",types,", groupOpt:",groupOpt,", deleteOpt:",deleteOpt

startDate=str(datetime.datetime.now().day-1)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().year)[2:]
fileName="summary_"+datetime.datetime.now().strftime("%Y-%m-%d")+".png"

if "True" in noPlot or "true" in noPlot:
    print subprocess.check_output(['python','plotInfo.py','--robos'] + roboIDs + ['--type'] + types +['--start',startDate,'--arguments']+tweetStrArgs)
else:
    print subprocess.check_output(['python','plotInfo.py','--robos'] + roboIDs + ['--type'] + types +['--start',startDate,'--save','True','--saveName',fileName,'--deleteOpt',deleteOpt,'--arguments']+tweetStrArgs)

    message = "Summary for "+str(datetime.datetime.now().day)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().year)[2:]+" #summary"
    tweet_image(message, fileName)

