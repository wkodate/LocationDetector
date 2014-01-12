#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import secret

class twitterapi:
    def __init__(self):
        self.api = twitter.Api( 
            consumer_key        = secret.dict['CONSUMER_KEY'],
            consumer_secret     = secret.dict['CONSUMER_SECRET'],
            access_token_key    = secret.dict['ACCESS_TOKEN'],
            access_token_secret = secret.dict['ACCESS_TOKEN_SECRET']
        )

    def verifyCredentials(self):
        return self.api.VerifyCredentials()

    def getUserTimeline(self, name='wkodate', cnt=20):
        statuses = self.api.GetUserTimeline(screen_name=name, count=cnt)
        for s in statuses:
            print s.text.encode('utf-8')

    def getTweetsWithLocoFromAccount(self, name='wkodate', cnt=20):
        statuses = self.api.GetUserTimeline(screen_name=name, count=cnt)
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
            # output file
