# roboTwitter

Python (tweepy) based scripts to read twitter feed ([@FriendPpe](https://twitter.com/FriendPpe)) and post plots to twitter feed
  * plot infromation: plotInfo.py
  * post information: postInfo.py
  * get information: getInfo.py
  * summarise information and post summary: summaryInfo.py

Example tweet:
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">test from afar T/H(C/%): 25.800001 / 42.400002 <a href="https://twitter.com/hashtag/tempHum?src=hash&amp;ref_src=twsrc%5Etfw">#tempHum</a> <a href="https://twitter.com/hashtag/RoboUno?src=hash&amp;ref_src=twsrc%5Etfw">#RoboUno</a></p>&mdash; kennys_ppe_friend (@FriendPpe) <a href="https://twitter.com/FriendPpe/status/1030040602698817536?ref_src=twsrc%5Etfw">August 16, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


### Python code

Required python libraries:
  * matplotlib
  * colorterm
  * tweepy

### Arduino code

Arduinos use DHT22 temperature-humidity sensor connected to:
  * Uno: use code EtherTweeter
  * 8266: use code WiFiTweeter  

