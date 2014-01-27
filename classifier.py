#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import yahoosplitter as splitter
from pysqlite2 import dbapi2 as sqlite

class classifier:
    def __init__(self, getfeatures, filtername=None):
        # 特徴/カテゴリのカウント
        self.fc={}
        # それぞれのカテゴリ中のドキュメント数
        self.cc = {}
        self.getfeatures = getfeatures

    def setdb(self,dbfile):
        self.con = sqlite.connect(dbfile)    
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')

    # 特徴/カテゴリのカウントを増やす
    def incFeature(self, f, cat):
        count = self.featureCount(f, cat)
        if count == 0:
            self.con.execute("insert into fc values ('%s','%s',1)" 
                    % (f, cat))
        else:
            self.con.execute(
                "update fc set count=%d where feature='%s' and category='%s'" 
                    % (count+1, f, cat)) 

    def incCategory(self, cat):
        count = self.categoryCount(cat)
        if count == 0:
            self.con.execute("insert into cc values ('%s',1)" % (cat))
        else:
            self.con.execute("update cc set count=%d where category='%s'" 
                    % (count+1, cat))    

    def featureCount(self, f, cat):
        res = self.con.execute(
            'select count from fc where feature="%s" and category="%s"'
            %(f, cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])

    # あるカテゴリ中のアイテムたちの数
    def categoryCount(self, cat):
        res = self.con.execute('select count from cc where category="%s"'
                %(cat)).fetchone()
        if res == None: return 0
        else: return float(res[0])

    # アイテムたちの総数
    def totalCount(self):
        res = self.con.execute('select sum(count) from cc').fetchone();
        if res == None: return 0
        return res[0]

    # すべてのカテゴリたちのリスト
    def categories(self):
        cur=self.con.execute('select category from cc');
        return [d[0] for d in cur]

    def train(self, item, cat):
        features = self.getfeatures(item)
        # このカテゴリ中の特徴たちのカウントを増やす
        for f in features:
            self.incFeature(f, cat)
        # このカテゴリのカウントを増やす
        self.incCategory(cat)
        self.con.commit()

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

def escape (self, s, quoted=u'.^$*+?', escape=u"\\"):
    return re.sub(u'[%s]' % re.escape(quoted), lambda mo: escape + mo.group(), s)

def sampletrain(cl, text, sex):
    for t in text:
        if len(t) == 0:
            continue
        t = re.sub(r'\'', '\'\'', t) 
        cl.train(t, sex)

    #cl.train(u'懐かしい衣装😂💛 #リクアワ #2014 #25 http://instagram.com/p/jmMRkIQFPS/ ','female')
    #cl.train(u'障がい児の社会参加の機会促進を目指し、ICTを活用した学習・生活支援研究「魔法のプロジェクト 2014 ～魔法のワンド～」の協力校を募集開始しました　http://goo.gl/NSn4Fh ','male')
    #cl.train(u'可愛かった話。 昨日、大竹まことさんがご自身のiPadをいじっているのを見ていたら、iPadカバーの内側に、なんと、マジックで大きくAppleIDとパスワードが書いてあった。 『大竹さんwwそれ絶対やったらダメなやつww』と教えても 『え？なんで？』とポカーン。 カワユス','female')
    #cl.train(u'本日ラジオ。英国紳士の昼下がりというイメージでやっています。。。','male')
    #cl.train(u'無料で新聞記事を読める『新聞＊全紙無料』で効率的に情報を仕入れる http://ift.tt/1hzfH8M','none')

