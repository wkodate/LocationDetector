#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import json
import twitter
import secret

class twitterapi:
    def __init__(self):
        self.twitterApi = twitter.Api( 
            consumer_key        = secret.dict['CONSUMER_KEY'],
            consumer_secret     = secret.dict['CONSUMER_SECRET'],
            access_token_key    = secret.dict['ACCESS_TOKEN'],
            access_token_secret = secret.dict['ACCESS_TOKEN_SECRET']
        )
        self.yahooApiAppId = secret.dict['APP_ID']
        self.terms = secret.terms

    def verifyCredentials(self):
        return self.twitterApi.VerifyCredentials()

    def getUserTimeline(self, name='wkodate', cnt=20):
        return self.twitterApi.GetUserTimeline(screen_name=name, count=cnt)

    def getSearch(self, tm, cnt=200):
        return self.twitterApi.GetSearch(term=tm, count=cnt)

    def showTweets(self, statuses):
        for s in statuses:
            print s.text.encode('utf-8')

    def showUserKeyphrase(self, statuses):
        for s in statuses:
            self.extractKeyphrase(s.text)

    def showTweetsWithLoco(self, statuses):
        tweets = {}
        tweets['texts'] = []
        tweets['full_names'] = []
        tweets['lat'] = []
        tweets['lng'] = []
        tweets['created_at'] = []
        for s in statuses:
            if (s.place is None):
                continue
            if (s.coordinates is None):
                continue
            lat = s.coordinates['coordinates'][0]
            lng = s.coordinates['coordinates'][1]

            tweets['texts'].append(s.text)
            tweets['full_names'].append(s.place['full_name'])
            tweets['lat'].append(lat)
            tweets['lng'].append(lng)
            tweets['created_at'].append(s.created_at)

            print '[text]'+s.text.encode('utf-8')
            print '[place]'+s.place['full_name'].encode('utf-8')
            print "[geo] %f %f" % (lat, lng)
            print "[created_at]"+s.created_at
            print '-----------------------------------'

    def extractKeyphrase(self, text):
        url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
        # remove reply user's name
        text = re.sub(r'@\w+ ', '', text.encode('utf-8'))

        sentence = urllib.quote_plus(text)
        query = "%s?appid=%s&output=%s&sentence=%s" % (url, self.yahooApiAppId, "json", sentence)
        c = urllib2.urlopen(query)
        json_str = c.read()
        result = json.loads(json_str)
        if len(result) == 0:
            return
        for k,v in sorted(result.items(), key=lambda x:x[1], reverse=True):
            print k.encode("utf-8")
