import tweepy
from datetime import datetime, date, time
import time
import configSettings

from termcolor import cprint
import matplotlib.pyplot as plt

import argumentClass

### get the inputs
args = argumentClass.GetArgs()
print args

robots=["roboUno", "robo8266"]
### basic dictiionary of parameters
### defaults as of August 2018 --> 'tweetArgs'=[4], 'types':["temp"], 'robos':["roboUno", "robo8266"]
plotDict={'robos':robots, 'types':["temp"], 'start':"NYS", 'end':"NYS", 'groupOpt':"NYS", 'deleteOpt':"NYS", 'tweetArgs':[4], 'pages':-1, 'save':"False", 'saveName':"NYS"}

### set parameters
for p in plotDict.keys():
    for k in vars(args).iteritems():
        if p in k[0] and not k[1]==None:
            print "got",k
            plotDict[p]=k[1]

### formating parameters
if not "NYS" in plotDict['start']:
    try:
        plotDict['start']=datetime.strptime(plotDict['start'],'%d-%m-%y')
    except:
        plotDict['start']=datetime.strptime("01-01-01",'%d-%m-%y')
else:
    plotDict['start']=datetime.strptime("01-01-01",'%d-%m-%y')

if not "NYS" in plotDict['end']:
    plotDict['end']=datetime.strptime(plotDict['end'],'%d-%m-%y')
else:
    plotDict['end']=datetime.today()

if plotDict['save']=="True" or plotDict['save']=="true":
    if "NYS" in plotDict['saveName']:
        plotDict['saveName']="summary_"+datetime.now().strftime("%Y-%m-%d")+".png"
    if not "." in plotName:
        plotDict['saveName']=plotDict['saveName']+".png"



if len(plotDict['robos'])<1 or len(['types'])<1:
    print "please set robo ["+", ".join([r for r in robots])+"] and type (e.g. temp) arguments"


#check for roboIDs
foundRobo=False
for id in plotDict['robos']:
    for r in robots:
        if id in r:
            foundRobo=True
            break
if foundRobo==False:
    print "robot IDs not found in:",robots
    exit()


print plotDict
#exit()

def GleanTwitter(argDict):

    deletedTweets=0
    api=configSettings.get_api()
    print "\n%%% time check: "+str(datetime.now())
    # get posts
    pageNum=0 #loop over pages
    pageLimit=argumentClass.Str2Int(argDict['pages'],"pageLimit")


    infoArr=[] #save gleaned info
    while True:
        #retrieve tweets aka status list
        statList=api.user_timeline(id="FriendPpe",page=pageNum)
        #print "\tpage",pageNum,"size of statList:",len(statList)
        if statList:
            for s in statList:
                if s.created_at < argDict['start'] or s.created_at > argDict['end']:
                    continue
                hashCheck=0
                rid="NYS"
                tid="NYS"
                #filter by hashtags to get info 
                for h in s.entities['hashtags']:
                    if "Problem" in h['text']:
                        hashCheck=-1
                        break
                    #check robots
                    for id in argDict['robos']:
                        if id in h['text']:
                            hashCheck+=1
                            rid=id
                            break
                        if "8266" in id and "2866" in h['text']: #fudge for being a tube!
                            hashCheck+=1
                            rid="8266"
                            break
                    #check types
                    for t in argDict['types']:
                        if t in h['text']:
                            hashCheck+=1
                            tid=t
                            break
                # throw away if hashtags don't match
                if hashCheck<2:
                    continue
                #print s.text
                #print s.created_at
                
                #dependant on formatting but for the moment...
                vals=[]
                noFloat=False
                for ta in argDict['tweetArgs']:
                    index=argumentClass.Str2Int(ta,"tweetArgs")
                    if index==-1:
                        continue
                    val=s.text.split(" ")[index]
                    #print "val:",val
                    try:
                        val=float(val)
                    except ValueError:
                        #skip tweet if format is not recognised
                        print "argument",int(ta),"of string not a float"
                        noFloat=True
                        continue
                    vals.append(val)
        
                #throw away if any data missing
                if noFloat: continue
                #add value to dateVal collection
                infoArr.append({'date':s.created_at, 'vals':vals, 'rid':rid, 'tid':tid})
                if argDict['deleteOpt']=="True" or argDict['deleteOpt']=="true":
                    api.destroy_status(s.id)
                    deletedTweets=deletedTweets+1
        else:
            #print "no statList"
            break

        if pageLimit>-1 and pageNum>=pageLimit:
            break
        pageNum+= 1
        print "next page:",pageNum


    print "GleanTwitter finds",len(infoArr),"data points"
    if argDict['deleteOpt']=="True" or argDict['deleteOpt']=="true":
        print "deleted tweets:",deletedTweets    

    return infoArr

def PlotData(argDict, infoArr):

    #group data from different types
    typeGroup=argDict['types']
    if "t" in argDict['groupOpt']:
        typeGroup=[""] # anything goes
    #group data from different robo IDs
    roboGroup=argDict['robos']
    if "r" in argDict['groupOpt']:
        roboGroup=[""] # anything goes

    plotList=[]
    if "d" in argDict['groupOpt']:
        plotList=[]
        for i in infoArr:
            foundDate=False
            for p in plotList:
                if i['date'].day==p[0]['date'].day:
                    foundDate=True
                    p.append(i)
                    break
            if foundDate==False:
                plotList.append([i])
    else:
        plotList=[infoArr]

    print "infoArr size:", len(infoArr)
    print "plotList size:", len(plotList)
    print "total plotList size:", sum([len(p) for p in plotList])

    plt.figure("time trend for"+"".join(argDict['types']))
    for p in plotList:
        for tid in typeGroup:
            for rid in roboGroup:
                for ta in range(0,len(argDict['tweetArgs']),1):
                    label=tid+" "+rid
                    if len(argDict['tweetArgs'])>1:
                        label=label+"("+str(ta)+")"
                    if "d" in argDict['groupOpt']:
                        label=label+": "+p[0]['date'].strftime("%d-%m-%y")
                    plt.plot([d['date'] for d in p if tid in d['tid'] and rid in d['rid']], [d['vals'][ta] for d in p if tid in d['tid']and rid in d['rid']], label=label)
    plt.gcf().autofmt_xdate()
    plt.xlabel("timeline")
    plt.ylabel("".join(argDict['types']))
    plt.legend(loc='best')

    if argDict['save']=="True" or argDict['save']=="true":
        plt.savefig(argDict['plotName'])
    else:
        plt.show()



twitterInfo=GleanTwitter(plotDict)


PlotData(plotDict,twitterInfo)
    
exit()
