#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import twitterapi
import classifier

argvs = sys.argv
argc = len(argvs)

def printDebug():
    print 'Usage: python %s account' % argvs[0]
    quit()

if argc != 2: 
    printDebug()

account = argvs[1]
count   = 200

t=twitterapi.twitterapi()
print account+' is ...'
statuses = t.getUserTimeline(account, count)
textList=t.getTweets(statuses)
textString=twitterapi.list2String(textList)

cl=classifier.fisherclassifier(classifier.getwords)
cl.setdb('test.db')
print cl.classify(textString)


