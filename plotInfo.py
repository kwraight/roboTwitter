### glean information from twitter and make plot
import tweepy
from datetime import datetime, date, time
import time
import copy

from termcolor import cprint
import matplotlib.pyplot as plt

import argumentClass
import sys
sys.path.insert(0, '../configs/')
import configSettings_ppe as configSettings


###############################
### USEFUL FUNCTIONS
###############################

def FormatDict(argDict):

    robots=["roboUno", "robo8266", "roboPi"]

    ### formatting parameters
    if "datetime" not in str(type(argDict['start'])):
        if "str" in str(type(argDict['start'])) and not "NYS" in argDict['start']:
            try:
                argDict['start']=datetime.strptime(argDict['start'],'%d-%m-%y')
            except:
                argDict['start']=datetime.strptime("01-01-01",'%d-%m-%y')
        else:
            argDict['start']=datetime.strptime("01-01-01",'%d-%m-%y')

    if "datetime" not in str(type(argDict['end'])):
        if "str" in str(type(argDict['end'])) and not "NYS" in argDict['end']:
            argDict['end']=datetime.strptime(argDict['end'],'%d-%m-%y')
        else:
            argDict['end']=datetime.today()

    if argDict['save']=="True" or argDict['save']=="true":
        if "NYS" in argDict['saveName']:
            argDict['saveName']="summary_"+datetime.now().strftime("%Y-%m-%d")+".png"
        if not "." in argDict['saveName']:
            argDict['saveName']=argDict['saveName']+".png"

    if "NYS" not in argDict['saveName']:
        argDict['save']="True"

    if len(argDict['robos'])<1 or len(['types'])<1:
        print "please set robo ["+", ".join([r for r in robots])+"] and type (e.g. temp) arguments"

    #check for roboIDs
    foundRobo=False
    for id in argDict['robos']:
        for r in robots:
            if id in r:
                foundRobo=True
                break
    if foundRobo==False:
        print "robot IDs not found in:",robots
        exit()

    #print "### argument dictionary\n",argDict

    return argDict

def GleanTwitter(argDict, opt="values"):

    deletedTweets=0
    api=configSettings.get_api()
    print "\n%%% time check: "+str(datetime.now())
    # get posts
    pageNum=0 #loop over pages
    pageLimit=argumentClass.Str2Int(argDict['pages'],"pageLimit")


    infoArr=[] #save gleaned info
    delArr=[]
    count=0
    loopGood=True
    while loopGood:
        #retrieve tweets aka status list
        statList=api.user_timeline(id=argDict['who'],page=pageNum)
        #print "\tpage",pageNum,"size of statList:",len(statList)
        if statList:
            for s in statList:
                if s.created_at > argDict['end']:
                    continue
                if s.created_at < argDict['start']:
                    loopGood=False
                    print s.created_at,"earlier than",argDict['start']
                    break
                hashCheck=0
                rid="NYS"
                tid="NYS"
                #filter by hashtags to get info 
                for h in s.entities['hashtags']:
                    if "Problem" in h['text']:
                        hashCheck=-100
                        break
                    if "summary" in h['text']:
                        hashCheck=0
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
                    if argDict['deleteOpt']=="True" or argDict['deleteOpt']=="true":
                        if hashCheck<0: # save the summaries
                            delArr.append(s.id)
                    continue
                #print s.text
                #print s.created_at
                
                if "val" in opt:
                    if argDict['noValues']=="True" or argDict['noValues']=="true":
                        count+=1
                        continue
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
                    count+=1

                else:
                    count+=1
                
                if argDict['deleteOpt']=="True" or argDict['deleteOpt']=="true":
                    delArr.append(s.id)

        else:
            #print "no statList"
            break

        if pageLimit>-1 and pageNum>=pageLimit:
            break
        pageNum+= 1
        print "next page:",pageNum,", from:",s.created_at


    print "GleanTwitter finds {0} data points in {1} pages ".format(count,pageNum)
    if argDict['deleteOpt']=="True" or argDict['deleteOpt']=="true":
        for d in delArr:
            api.destroy_status(d)
        print "deleted tweets:",len(delArr)

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

    if sum([len(p) for p in plotList])<1:
        print "nothing to plot!"
        return

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
        print "PlotData: saving (not showing)",argDict['saveName']
        plt.savefig(argDict['saveName'])
    else:
        plt.show()

    return argDict['saveName']


###############################
### EXECUTE
###############################

def main():
    print ">>>plotInfo running..."

    ### basic dictionary of parameters
    ### defaults as of August 2018 --> 'tweetArgs'=[4], 'types':["temp"], 'robos':["roboUno", "robo8266"]
    plotDict=copy.deepcopy(argumentClass.templatePlotDict)
    #{'robos':["Uno","8266"], 'types':["temp"], 'start':"NYS", 'end':"NYS", 'groupOpt':"NYS", 'deleteOpt':"NYS", 'tweetArgs':[4], 'pages':-1, 'save':"False", 'saveName':"NYS"}

    ### get the inputs
    args = argumentClass.GetArgs()
    #print args

    ### set parameters
    for p in plotDict.keys():
        for k in vars(args).iteritems():
            if p in k[0] and not k[1]==None:
                print "got",k
                plotDict[p]=k[1]

    plotDict={'groupOpt': 'NYS', 'saveName': 'plots/summary_2018-08-26.png', 'end': datetime(2018, 8, 26, 23, 29, 45, 150624), 'deleteOpt': 'NYS', 'robos': ['Uno', '8266'], 'who': 'FriendPpe', 'start': datetime(2018, 8, 25, 23, 29, 45, 150605), 'tweetArgs': [4], 'save': 'False', 'pages': -1, 'types': ['temp'], 'noValues': 'False'}


#plotDict=FormatDict(plotDict)

    print "### plotDict:\n",plotDict

    tweetArr=GleanTwitter(plotDict, "values")


    PlotData(plotDict,tweetArr)
    print ">>>plotInfo finished."

if __name__ == "__main__":
    main()
    exit()



