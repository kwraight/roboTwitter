
import tweepy
# Fill in the values noted in previous step here
cfg = {
    "consumer_key"        : "YOUR_INFO_HERE",
    "consumer_secret"     : "YOUR_INFO_HERE",
    "access_token"        : "YOUR_INFO_HERE",
    "access_token_secret" : "YOUR_INFO_HERE"
}

#twitter guy
def get_api():
    global cfg
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)
