# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:26:19 2020

@author: lenovo
"""


from aip import AipNlp
import pandas as pd
import time

APP_ID = '19393497'
API_KEY = 'yPdk9l0GyGjzIRDv7TDa6zKj'
SECRET_KEY = 'W2Pwr0j0lPhQ17akkVAxQkmVF9qGe01Q'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#text = "[闭嘴][闭嘴][闭嘴][闭嘴][闭嘴][闭嘴][闭嘴][闭嘴][闭嘴]"
#
#""" 调用情感倾向分析 """
#ans=client.sentimentClassify(text)
#senti=ans['items'][0]['sentiment']
#print(ans,senti)

print('start')
start_time=time.clock()
data=pd.read_csv(r'../data/new_test300_result_verify.csv')
danmu=data['danmu'].tolist()
baidu_ans=[]
for i in danmu:
    try:
        ans=client.sentimentClassify(i)
        senti=ans['items'][0]['sentiment']-1
        print(i,senti)
        baidu_ans.append(senti)
    except:
        baidu_ans.append(8)
    time.sleep(1)    

end_time=time.clock()
print('time:',end_time-start_time)
data['baidu']=baidu_ans
data.to_csv(r'../data/baidu_new_test300_result_verify.csv',index=None)
#389s
    