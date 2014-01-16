 # -*- coding: UTF-8 -*-
import twitter
import secret
import locoTweets
from django.template import Context, loader
from django.http import HttpResponse
 
def home(req):
    api = getApi()
    terms = secret.terms

    tweets = []
    for tm in terms:
        statuses = api.GetSearch(term=tm, count=200)
        if (statuses is None) :
            continue
        for s in statuses:
            if (s.place is None):
                continue
            if (s.coordinates is None):
                continue

            tweet = extractStatusFields(s)
            printTweet(tweet) 
            tweets.append(tweet)

    t = loader.get_template('views.html')
    c = Context({
        'tweets': tweets,
    })
    return HttpResponse(t.render(c))

def getApi():
    return twitter.Api( 
        consumer_key        = secret.dict['CONSUMER_KEY'],
        consumer_secret     = secret.dict['CONSUMER_SECRET'],
        access_token_key    = secret.dict['ACCESS_TOKEN'],
        access_token_secret = secret.dict['ACCESS_TOKEN_SECRET']
    )

def extractStatusFields(status):
    tweet = {}
    tweet['user']       = status.user.screen_name
    tweet['texts']      = status.text.replace('\n', '').replace('\r', '')
    tweet['full_names'] = status.place['full_name']
    tweet['lat']        = status.coordinates['coordinates'][0]
    tweet['lng']        = status.coordinates['coordinates'][1]
    return tweet

def printTweet(tweet):
    print '[user]'+tweet['user'].encode('utf-8')
    print '[text]'+tweet['texts'].encode('utf-8')
    print '[place]'+tweet['full_names'].encode('utf-8')
    print "[geo] %f %f" % (tweet['lat'], tweet['lng'])
    print '-----------------------------------'

