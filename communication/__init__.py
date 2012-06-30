'''This app is for communication with outside services.

The intent is for this app to manage aggregation of external API's such as twitter, google+ and facebook.
User specific API settings, such as keys are stored in localsettings.py in the root directory.


Here is some example code for Twitter (see https://dev.twitter.com/docs/embedded-tweets)

import urllib, urllib2
import json


#this downloads the timeline for a user
TWITTER_NAME = 'dave_bridges'
values = {'screen_name':TWITTER_NAME, 'count':200, 'rts':'true', 'trim_user':'true', 'exclude_replies':'true'}
params = urllib.urlencode(values)
target_site = 'https://api.twitter.com/1/statuses/user_timeline.json?' + params
response = urllib2.urlopen(target_site)
json_response = response.read() #this reads the HTTP response
timeline = json.loads(json_response)
timeline[0]['created_at']
timeline[0]['user']
for tweet in timeline:
    print tweet['text']
'''