__author__ = 'apple'
# -*- coding:utf-8 -*-

import word2vec

orginFile = 'positive_2.csv'
word2vec.word2phrase(orginFile, orginFile+"-phrases", verbose=True)
word2vec.word2vec(orginFile+"-phrases",orginFile+".bin",size=50,verbose=True)
word2vec.word2clusters(orginFile,orginFile+"-clusters.txt",50,verbose=True)
model = word2vec.load(orginFile+".bin")
s = '王'.decode('utf-8').encode()
print(s)
print(model[s].shape)
