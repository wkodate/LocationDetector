#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import urllib2
import re
import json

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

    def getUserTimelineFromAccount(self, name='wkodate', cnt=20):
        statuses = self.twitterApi.GetUserTimeline(screen_name=name, count=cnt)
        for s in statuses:
            print s.text.encode('utf-8')

    def getTweetsWithLocoFromAccount(self, name='wkodate', cnt=20):
        statuses = self.twitterApi.GetUserTimeline(screen_name=name, count=cnt)
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
            tweets['texts'].append(s.text)
            tweets['full_names'].append(s.place['full_name'])
            lat = s.coordinates['coordinates'][0]
            lng = s.coordinates['coordinates'][1]
            tweets['lat'].append(lat)
            tweets['lng'].append(lng)
            tweets['created_at'].append(s.created_at)

            print '[text]'+s.text.encode('utf-8')
            print '[place]'+s.place['full_name'].encode('utf-8')
            print "[geo] %f %f" % (lat, lng)
            print "[created_at]"+s.created_at
            print '-----------------------------------'

    def searchTweetsFromTerm(self, tm, cnt=200):
        statuses = self.twitterApi.GetSearch(term=tm, count=cnt)
        for s in statuses:
            if (s.place is None):
                continue
            print s.text.encode('utf-8')
            print s

    def searchTweetsFromList(self, cnt=200):
        for tm in self.terms:
            statuses = self.twitterApi.GetSearch(term=tm, count=cnt)
            if (statuses is None) :
                continue
            for s in statuses:
                if (s.place is None):
                    continue
                print s.text.encode('utf-8')
                print s.place['full_name'].encode('utf-8')
                print s                

    def keyphrase(self, name='wkodate', cnt=50):
        url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
        statuses = self.twitterApi.GetUserTimeline(screen_name=name, count=cnt)
        for s in statuses:
            text = re.sub(r'@\w+ ', '', s.text.encode('utf-8'))
            print text

            sentence = urllib.quote_plus(text)
            query = "%s?appid=%s&output=%s&sentence=%s" % (url, self.yahooApiAppId, "json", sentence)
            c = urllib2.urlopen(query)
            json_str = c.read()
            result = json.loads(json_str)
            if len(result) == 0:
                continue;
            for k,v in sorted(result.items(), key=lambda x:x[1], reverse=True):
                print "keyphrase:%s, score:%d" % (k.encode("utf-8"), v)
            print '-----------------------------------'
