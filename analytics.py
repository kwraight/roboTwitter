### glean information from twitter and make plot
import tweepy
from datetime import datetime, date, time
import time
import ../configSettings_pwd
import matplotlib.pyplot as plt
import numpy as np
import argumentClass


###############################
### USEFUL FUNCTIONS
###############################


def checkTopics(topArr, top, type="NYS"):

    foundTop=False
    for t in topArr:
        if top==t['name'] and type==t['type']:
            foundTop=True
            t['num']+=1
            break

    if not foundTop:
        topArr.append({'name':top,'num':1, 'type':type})

def FormatDict(argDict):
    
    
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


def GleanTwitter(argDict):
    
    topics=[]

    api=configSettings_pwd.get_api()
    print "\n%%% time check: "+str(datetime.now())
    # get posts
    pageNum=0 #loop over pages
    pageLim=argumentClass.Str2Int(argDict['pages'],"pageLimit")
    count=0

    while True:
        #retrieve tweets aka status list
        statList=api.user_timeline(id=argDict['who'],page=pageNum) #FriendPpe
        #print "\tpage",pageNum,"size of statList:",len(statList)
        if statList:
            for s in statList:
                if s.created_at < argDict['start'] or s.created_at > argDict['end']:
                    continue
                try:
                    statTxt=s.text.encode('ascii', 'ignore')
                    count+=1
                except:
                    continue
                
                if "h" in argDict['topics']:
                    for h in s.entities['hashtags']:
                        #print "hashtag:",h['text']
                        checkTopics(topics,h['text'],"h")
                if "s" in argDict['topics']:
                    for h in s.entities['symbols']:
                        #print "symbol:",h['text']
                        checkTopics(topics,h['text'],"s")
                if "n" in argDict['topics']:
                    for h in s.entities['user_mentions']:
                        #print "mention:",h['name'].encode('ascii', 'ignore'),"(",h['screen_name'].encode('ascii', 'ignore'),")" #screen_name
                        checkTopics(topics,h['name'].encode('ascii', 'ignore'),"n")
        else:
            #print "no statList"
            break

        pageNum+=1
        if pageLim>0 and pageNum>=pageLim:
            break
        print "...next page:",pageNum
        
        
    print "topics:",len(topics),"in",count,"tweets"
    print topics
    print "highest instance:", max(topics, key=lambda x:x['num'])
    return topics

def PlotFreq(topArr):

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors=colors*((len(topArr)/len(colors))+1)
    
    fig, ax = plt.subplots()
    ind = np.arange(1,len(topArr)+1)
    plots = plt.bar(ind, [t['num'] for t in topArr])
    for p,c in zip(plots,colors):
        p.set_facecolor(c)
    ax.set_xticks(ind)
    ax.set_xticklabels([t['name']+"("+t['type']+")" for t in topArr],rotation = 45, ha="right")
    ax.set_ylim([0, max([t['num'] for t in topArr])*1.05])
    ax.set_ylabel('frequency')
    ax.set_title('topic frequency from '+str(len(topArr))+' tweets')
    plt.tight_layout()
    #plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95, hspace=0.40, wspace=0.409) # plots layout

    plt.show()

###############################
### EXECUTE
###############################

def main():
    print ">>>analytics running..."


    args = argumentClass.GetArgs()
    
    ### set parameters
    argDict={'who':"FriendPpe", 'start':"01-01-01", 'end':datetime.now(), 'pages':"-1", 'topics':"nhs"}
    for k in vars(args).iteritems():
        if not k[1]==None:
            print "got",k
            argDict[k[0]]=k[1]

    FormatDict(argDict)
    print argDict


    topArr=GleanTwitter(argDict)
    PlotFreq(topArr)
    print ">>>analytics finished."

if __name__ == "__main__":
    main()
    exit()



