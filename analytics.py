### glean information from twitter and make plot
import tweepy
from datetime import datetime, date, time
import time
import configSettings
import matplotlib.pyplot as plt
import numpy as np


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

def GleanTwitter(who="red_hot_kenny",pageLim=1):
    

    topics=[]

    api=configSettings.get_api()
    print "\n%%% time check: "+str(datetime.now())
    # get posts
    pageNum=0 #loop over pages
    count=0

    while True:
        #retrieve tweets aka status list
        statList=api.user_timeline(id=who,page=pageNum) #FriendPpe
        #print "\tpage",pageNum,"size of statList:",len(statList)
        if statList:
            for s in statList:
                try:
                    statTxt=s.text.encode('ascii', 'ignore')
                    count+=1
                except:
                    continue
                
                for h in s.entities['hashtags']:
                    #print "hashtag:",h['text']
                    checkTopics(topics,h['text'],"h")
                for h in s.entities['symbols']:
                    #print "symbol:",h['text']
                    checkTopics(topics,h['text'],"s")
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
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95, hspace=0.40, wspace=0.409) # plots layout

    plt.show()

###############################
### EXECUTE
###############################

def main():
    print ">>>analytics running..."

    topArr=GleanTwitter()# "FriendPpe",-1)
    PlotFreq(topArr)
    print ">>>analytics finished."

if __name__ == "__main__":
    main()
    exit()



