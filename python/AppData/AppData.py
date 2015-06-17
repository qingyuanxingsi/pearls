__author__ = 'apple'
#-*- encoding:utf-8 -*-

APP_DATA_PATH = r'/home/apple/data/guangzhou/信用等级模型+MM/201405/tmh_user_credit_level_m201405_1.txt'

tag = 0
for line in open(APP_DATA_PATH):
    if tag<10:
        tag+=1
        print line
    else:
        break
