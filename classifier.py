#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yahoosplitter as splitter

class classifier:
    def __init__(self, getfeatures, filtername=None):
        # 特徴/カテゴリのカウント
        self.fc={}
        # それぞれのカテゴリ中のドキュメント数
        self.cc = {}
        self.getfeatures = getfeatures

    # 特徴/カテゴリのカウントを増やす
    def incFeature(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incCategory(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def featureCount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # あるカテゴリ中のアイテムたちの数
    def categoryCount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # アイテムたちの総数
    def totalCount(self):
        return sum(self.cc.values())

    # すべてのカテゴリたちのリスト
    def categories(self):
        return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        # このカテゴリ中の特徴たちのカウントを増やす
        for f in features:
            self.incFeature(f, cat)
        # このカテゴリのカウントを増やす
        self.incCategory(cat)

    def featureProb(self, f, cat):
        if self.categoryCount(cat) == 0: return 0
        # このカテゴリの中にこの特徴が出現する回数を
        # このカテゴリ中のアイテム総数で割る
        return self.featureCount(f, cat) / self.categoryCount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob=prf(f,cat)
        
        # Count the number of times this feature has appeared in
        # all categories
        totals=sum([self.featureCount(f,c) for c in self.categories()])
        
        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

class naivebayes(classifier):
  
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.thresholds = {}
    
    def docprob(self, item, cat):
        features = self.getfeatures(item)   
        
        # すべての特徴の確率を掛け合わせる
        p = 1
        for f in features: p *= self.weightedprob(f, cat, self.featureProb)
        return p

    def prob(self,item,cat):
        catprob=self.categoryCount(cat)/self.totalCount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t
      
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]
    
    def classify(self,item,default=None):
        probs={}
        # もっとも確率の高いカテゴリを探す
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max: 
                max=probs[cat]
                best=cat
        
        # 確率がしきい値*2番目にベストなものを超えているか確認する
        for cat in probs:
            if cat==best: continue
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best

def getwords(doc):
    words = [s.lower() for s in splitter.split(doc) 
            if len(s)>2 and len(s)<20]
    # ユニークな単語の集合を返す
    return dict([(w, 1) for w in words])

