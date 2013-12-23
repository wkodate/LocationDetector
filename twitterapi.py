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

