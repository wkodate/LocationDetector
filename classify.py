#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import twitterapi
import classifier

argvs = sys.argv
argc = len(argvs)
if argc != 2: 
    print 'Usage: python %s account' % argvs[0]
    quit()

t=twitterapi.twitterapi()
print argvs[1]+' is ...'
statuses = t.getUserTimeline(argvs[1], 200)
textList=t.getTweets(statuses)
textString=twitterapi.list2String(textList)

cl=classifier.fisherclassifier(classifier.getwords)
cl.setdb('test.db')
print cl.classify(textString)
