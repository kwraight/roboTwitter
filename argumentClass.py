# basic argument list definition & parsing and useful functions
from datetime import datetime, date, time
import configSettings
import argparse

def Str2Int(theStr,refStr=""):
    try:
        return int(theStr)
    except ValueError:
        print refStr+" string \'"+theStr+"\' cannot be cast as int"
    except:
        print refStr+" string \'"+theStr+"\' is not recognise"
    return -1

templatePlotDict={'who':"FriendPpe", 'robos':["Uno","8266"], 'types':["temp"], 'start':"NYS", 'end':"NYS", 'groupOpt':"NYS", 'deleteOpt':"NYS", 'tweetArgs':[4], 'pages':-1, 'save':"False", 'saveName':"NYS", 'noValues':"False"}

def GetArgs():
    ### get arguments for setting parameters
    parser = argparse.ArgumentParser(description="Arguments for roboTwitter functions")
    
    #basics
    parser.add_argument('--who', help='name of twitter account default:FriendPpe')
    parser.add_argument('--deleteOpt', help='delete used tweets')
    
    # info settings
    parser.add_argument('--robos', nargs='+', help='name of robot ')
    parser.add_argument('--types', nargs='+', help='measurement type, e.g. temp')
    parser.add_argument('--groupOpt', help='grouping for histogram: r - merge roboIDs; t - merge types; d split days')
    parser.add_argument('--arguments', nargs='+', help='argument selection: which (space separated) (inetger) arguments from tweet (default=4)')
    
    # loop limits
    parser.add_argument('--start', help='start date: dd-mm-yy')
    parser.add_argument('--end', help='end date: dd-mm-yy')
    parser.add_argument('--pages', help='how many pages to be used')
    
    # plotting
    parser.add_argument('--save', help='save plot: defaultName=\'summary_DATE\'')
    parser.add_argument('--saveName', help='plot name (if saving). Use png extension used if none given')
    parser.add_argument('--noTweet', help='suppress update twitter')
    parser.add_argument('--noValues', help='count only, no plots')
    
    # analytics
    parser.add_argument('--topics', help='include in string: n - names; h - hashtags; s - symbols')
    

    ### check the inputs
    args = parser.parse_args()
    
    return args

