#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import twitterapi
import classifier

argvs = sys.argv
argc = len(argvs)

def printDebug():
    print 'Usage: python %s account [male|female|other]' % argvs[0]
    quit()

if argc != 3 : 
    printDebug()
if argvs[2] != 'male' and argvs[2] != 'female' and argvs[2] != 'other':
    printDebug()

account = argvs[1]
sex = argvs[2]
count   = 200

t=twitterapi.twitterapi()
statuses = t.getUserTimeline(account, count)
textList=t.getTweets(statuses)

cl=classifier.fisherclassifier(classifier.getwords)
cl.setdb('test.db')
print 'Training ...'
classifier.sampletrain(cl, textList, sex)
print 'Success: '+account+' has been trained as '+sex
