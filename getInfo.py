import tweepy
from datetime import datetime, date, time
import time
import ../configSettings_ppe

from termcolor import cprint
import matplotlib.pyplot as plt
 


    counts={"stayCalm":0,"bareTeeth":0,"runAway":0}
    api=configSettings.get_api()
    while True:
        print "\n%%% time check: "+str(datetime.now())
        # get only 5 most recent posts
        statList=api.user_timeline(id="FriendPpe",page=0)[:5]
        print "\tsize of statList:",len(statList)
        for s in statList:
            #print s
            print s.text
            print s.created_at
            for h in s.entities['hashtags']:
                if "stayCalm" in h['text']:
                    counts['stayCalm']+=1
                    cprint(h['text'],'blue')
                elif "bareTeeth" in h['text']:
                    counts['bareTeeth']+=1
                    cprint(h['text'],'red')
                elif "runAway" in h['text']:
                    counts['runAway']+=1
                    cprint(h['text'],'green')
                else:
                    print h['text']
        total=sum([counts[key] for key in counts])
        plt.figure("props")
        plt.pie([float(counts[key])/total for key in counts], labels=[key for key in counts], autopct='%1.1f%%', shadow=True)
        plt.show(block=False)
        plt.pause(4)
        #time.sleep(10)
        plt.close('all')

if __name__ == "__main__":
    main()

