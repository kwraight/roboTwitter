import tweepy
from datetime import datetime, date, time
import time
import configSettings

from termcolor import cprint
#import matplotlib.pyplot as plt

import argumentClass

### check the inputs
args = argumentClass.GetArgs()
print args

#for k in vars(args).iteritems():
#    print k[1]

exit()
# them robots
robots=["robo8266","roboUno"]
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
    print "please set robo ["+", ".join([r for r in robots])+"] and type (e.g. temp) arguments"
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



def main():

    api=configSettings.get_api()
    print "\n%%% time check: "+str(datetime.now())
    # get posts
    pageNum=0
    dateVals=[]
    while True:
        statList=api.user_timeline(id="FriendPpe",page=pageNum)
        #print "\tpage",pageNum,"size of statList:",len(statList)
        if statList:
            for s in statList:
                if s.created_at < startDate or s.created_at > endDate:
                    continue
                hashCheck=0
                rid="NYS"
                tid="NYS"
                for h in s.entities['hashtags']:
                    if "Problem" in h['text']:
                        hashCheck=-1
                        
                        break
                    for id in roboIDs:
                        if id in h['text']:
                            hashCheck+=1
                            rid=id
                            break
                        if "8266" in id and "2866" in h['text']: #fudge for being a tube!
                            hashCheck+=1
                            rid="8266"
                            break
                    for t in types:
                        if t in h['text']:
                            hashCheck+=1
                            tid=t
                            break
                if hashCheck<2:
                    continue
                #print s.text
                #print s.created_at
                
                #dependant on formatting but for the moment...
                vals=[]
                noFloat=False
                for ta in tweetStrArgs:
                    val=s.text.split(" ")[ta]
                    #print "val:",val
                    try:
                        val=float(val)
                    except ValueError:
                        #skip tweet if format is not recognised
                        print "argument",ta,"of string not a float"
                        noFloat=True
                        continue
                    vals.append(val)
        
                if noFloat: continue
                #add value to dateVal collection
                dateVals.append({'date':s.created_at, 'vals':vals, 'rid':rid, 'tid':tid})
                if deleteOpt=="True" or deleteOpt=="true":
                    api.destroy_status(s.id)
                    global deletedTweets
                    deletedTweets=deletedTweets+1
                
                '''
                foundDate=False
                for dv in dateVals:
                    if dv[0]['date'].day==s.created_at.day:
                        foundDate=True
                        dv.append({'date':s.created_at, 'val':val, 'rid':rid, 'tid':tid})
                        break
                if foundDate==False:
                    dateVals.append([{'date':s.created_at, 'val':val, 'rid':rid, 'tid':tid}])
                    '''
                    
        else:
            break

        if pages>-1 and pageNum>=pages:
            break
        pageNum+= 1
        print "next page:",pageNum


    typeGroup=types
    if "t" in groupOpt:
        typeGroup=[""] # anything goes
    roboGroup=roboIDs
    if "r" in groupOpt:
        roboGroup=[""] # anything goes

    dateValsList=[]
    if "d" in groupOpt:
        dateValsList=[]
        for dv in dateVals:
            foundDate=False
            for dvl in dateValsList:
                if dv['date'].day==dvl[0]['date'].day:
                    foundDate=True
                    dvl.append(dv)
                    break
            if foundDate==False:
                dateValsList.append([dv])
    else:
        dateValsList=[dateVals]

    print "dateValsList size:", len(dateValsList)
    print "values size:", sum([len(dvl) for dvl in dateValsList])
    if deleteOpt=="True" or deleteOpt=="true":
        print "deleted tweets:",deletedTweets

    plt.figure("time trend")
    for dvl in dateValsList:
        for tid in typeGroup:
            for rid in roboGroup:
                for ta in range(0,len(tweetStrArgs),1):
                    label=tid+" "+rid
                    if len(tweetStrArgs)>1:
                        label=label+"("+str(ta)+")"
                    if "d" in groupOpt:
                        label=label+": "+dvl[0]['date'].strftime("%d-%m-%y")
                    plt.plot([d['date'] for d in dvl if tid in d['tid'] and rid in d['rid']], [d['vals'][ta] for d in dvl if tid in d['tid']and rid in d['rid']], label=label)
    plt.gcf().autofmt_xdate()
    plt.xlabel("timeline")
    plt.ylabel("".join([t for t in types]))
    plt.legend(loc='best')

    if save=="True" or save=="true":
        plotName=saveName
        #print "File:",saveName,"to be saved"
        if "NYS" in plotName:
            plotName="summary_"+datetime.now().strftime("%Y-%m-%d")+".png"
        if not "." in plotName:
            plotName=plotName+".png"
        plt.savefig(plotName)
    else:
        plt.show()



if __name__ == "__main__":
    main()
    
    exit()
