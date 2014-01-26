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
