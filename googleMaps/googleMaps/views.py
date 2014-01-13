 # -*- coding: UTF-8 -*-
import twitter
import secret
from django.template import Context, loader
import googleMaps
from django.http import HttpResponse
 
def home(req):
    api = twitter.Api( 
        consumer_key        = secret.dict['CONSUMER_KEY'],
        consumer_secret     = secret.dict['CONSUMER_SECRET'],
        access_token_key    = secret.dict['ACCESS_TOKEN'],
        access_token_secret = secret.dict['ACCESS_TOKEN_SECRET']
    )
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

            tweet = {}
            user_name = s.user.screen_name
            text = s.text
            text = text.replace('\n', '')
            text = text.replace('\r', '')
            place_name = s.place['full_name']
            lat = s.coordinates['coordinates'][0]
            lng = s.coordinates['coordinates'][1]

            tweet['user'] = user_name
            tweet['texts'] = text
            tweet['full_names'] = place_name
            tweet['lat'] = lat
            tweet['lng'] = lng
            tweets.append(tweet)

            print '[user]'+user_name.encode('utf-8')
            print '[text]'+text.encode('utf-8')
            print '[place]'+place_name.encode('utf-8')
            print "[geo] %f %f" % (lat, lng)
            print s                
            print '-----------------------------------'

    t = loader.get_template('views.html')
    c = Context({
        'tweets': tweets,
    })
    return HttpResponse(t.render(c))
