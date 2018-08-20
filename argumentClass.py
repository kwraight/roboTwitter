#
from datetime import datetime, date, time
import configSettings
import argparse


# them robots
robots=["robo8266","roboUno"]

def GetArgs():
    ### get arguments for setting parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--robos', nargs='+', help='name of robot: '+str(robots))
    parser.add_argument('--start', help='start date: dd-mm-yy')
    parser.add_argument('--end', help='end date: dd-mm-yy')
    parser.add_argument('--types', nargs='+', help='measurement type, e.g. temp')
    parser.add_argument('--groupOpt', help='grouping for histogram: r - merge roboIDs; t - merge types; d split days')
    parser.add_argument('--arguments', nargs='+', help='argument selection: which (space separated) (inetger) arguments from tweet (default=4,6)')
    parser.add_argument('--save', help='save plot: defaultName=\'summary_DATE\'')
    parser.add_argument('--saveName', help='plot name (if saving). Use png extension used if none given')
    parser.add_argument('--deleteOpt', help='delete used tweets')
    parser.add_argument('--pages', help='how many pages to be used')

    ### check the inputs
    args = parser.parse_args()
    return args

'''
### set parameters
roboIDs=[]
if not args.robos is None:
    roboIDs = args.robos
print "len:",len(roboIDs)

types=[]
if not args.types is None:
    types = args.types

startDate=datetime.strptime("01-01-01",'%d-%m-%y')
if not args.start is None:
    startDate = datetime.strptime(args.start,'%d-%m-%y')

endDate=datetime.now()
if not args.end is None:
    endDate = datetime.strptime(args.end,'%d-%m-%y')

groupOpt="NYS"
if not args.groupOpt is None:
    groupOpt = args.groupOpt

deleteOpt="NYS"
deletedTweets=0
if not args.deleteOpt is None:
    deleteOpt = args.deleteOpt

tweetStrArgs=[]
if not args.arguments is None:
    for a in args.arguments:
        try:
            tweetStrArgs.append(int(a))
        except:
            print "suggested argument",a,"not an integer"
else:
    tweetStrArgs=[4,6]

pages=-1
if not args.pages is None:
    try:
        pages = int(args.pages)
    except:
        pages=-1

save="False"
if not args.save is None:
    save = args.save

saveName="NYS"
if not args.saveName is None:
    saveName = args.saveName
    save="True"

if len(roboIDs)<1 or len(types)<1:
    print "please set robo and type arguments"
    exit()

print ">>> plotInfo parameters... \nroboIDs:",roboIDs,", types:",types,", start:",startDate,", end:",endDate,", groupOpt:",groupOpt,", deleteOpt:",deleteOpt,", save:",save,", saveName:",saveName,", tweetStrArgs:",tweetStrArgs,", pages:",pages

#check for roboIDs
foundRobo=False
for id in roboIDs:
    for r in robots:
        if id in r:
            foundRobo=True
            break
if foundRobo==False:
    print "robot IDs not found in:",robots
    exit()

'''

