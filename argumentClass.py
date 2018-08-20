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



def GetArgs():
    ### get arguments for setting parameters
    parser = argparse.ArgumentParser(description="Arguments for roboTwitter functions")
    parser.add_argument('--robos', nargs='+', help='name of robot ')
    parser.add_argument('--start', help='start date: dd-mm-yy')
    parser.add_argument('--end', help='end date: dd-mm-yy')
    parser.add_argument('--types', nargs='+', help='measurement type, e.g. temp')
    parser.add_argument('--groupOpt', help='grouping for histogram: r - merge roboIDs; t - merge types; d split days')
    parser.add_argument('--arguments', nargs='+', help='argument selection: which (space separated) (inetger) arguments from tweet (default=4)')
    parser.add_argument('--save', help='save plot: defaultName=\'summary_DATE\'')
    parser.add_argument('--saveName', help='plot name (if saving). Use png extension used if none given')
    parser.add_argument('--deleteOpt', help='delete used tweets')
    parser.add_argument('--pages', help='how many pages to be used')
    parser.add_argument('--noTweet', help='suppress update twitter')

    ### check the inputs
    args = parser.parse_args()
    
    return args

