# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:46:50 2020

@author: lenovo
"""

#基于词典的情感分析
import jieba
import os,time
from pyltp import Segmentor
from data_cleaning import *
from langconv import *
import pandas as pd


# 加载自定义词典
jieba.load_userdict(r'../dict/self_dict.txt')


LTP_DATA_DIR = r'../ltp_data_v3.4.0/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, r"../dict/self_dict.txt")  # 加载模型，第二个参数是您的外部词典文件路径

pos_dict=pd.read_csv(r'../dict/self_positive_dict.txt',header=None)
pos_dict=pos_dict[0].tolist()

neg_dict=pd.read_csv(r'../dict/self_negative_dict.txt',header=None)
neg_dict=neg_dict[0].tolist()

not_dict=pd.read_csv(r'../dict/self_not.txt',header=None)
not_dict=not_dict[0].tolist()

with open("../dict/self_degree.txt",'r',encoding='utf-8') as f:    
    degree=eval(f.read()) #把字典转化为str 

degree_most=degree['most']
degree_more=degree['more']
degree_less=degree['less']
degree_least=degree['least']

print('正面情感词:',len(pos_dict))
print('负面情感词:',len(neg_dict))
print('否定词:',len(not_dict))
print('程度副词:',len(degree_most),len(degree_more),len(degree_less),len(degree_least))

#数据清洗
def danmu_clean(sentence):
    with open(r"../dict/dyemot.txt", 'r')as f:
        emot_dict = eval(f.read())
        
    sentence=symbol_replace(sentence)
    sentence=tradition2simple(sentence)
    sentence=sim_replace(sentence)
    sentence=emoji_replace(sentence)
    
    return sentence


#jieba分词
def jieba_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
# 去多余空格
    for i in seg_list:
        if i==' ':
            continue
        else:
            seg_result.append(i)
    
    return seg_result

#ltp分词
def ltp_word(sentence):
    seg_result = segmentor.segment(sentence)
    return list(seg_result)


#计算情感得分    
def sentence_score(seg_result):
    pos_score=0
    neg_score=0
    
    for i in range(0,len(seg_result)):        
        if seg_result[i] in pos_dict:
#            print('pos:',seg_result[i])
            tmp=1
#            向前查1-2个词
            for j in [1,2]:
                if i-j<0:
                    break
#                有标点说明前后无联系，提前结束
                if seg_result[i-j]==',' or seg_result[i-j]=='.':
                    break
                else:
                    if seg_result[i-j] in not_dict:
                        tmp=tmp*-1
                        continue
                    elif seg_result[i-j] in degree_most:
                        tmp=tmp*1.75
                        continue
                    elif seg_result[i-j] in degree_more:
                        tmp=tmp*1.5
                        continue
                    elif seg_result[i-j] in degree_less:
                        tmp=tmp*0.75
                        continue
                    elif seg_result[i-j] in degree_least:
                        tmp=tmp*0.5
                        continue
            pos_score+=tmp
        elif seg_result[i] in neg_dict:
#            print('neg:',seg_result[i])
            tmp=1
#            向前查1-2个词
            for j in [1,2]:
                if i-j<0:
                    break
                if seg_result[i-j]==',' or seg_result[i-j]=='.':
                    break
                else:
                    if seg_result[i-j] in not_dict:
#                        负面词被否定词修饰视为无情感或略微正向
                        tmp=tmp*0
                        continue
                    elif seg_result[i-j] in degree_most:
                        tmp=tmp*1.75
                        continue
                    elif seg_result[i-j] in degree_more:
                        tmp=tmp*1.5
                        continue
                    elif seg_result[i-j] in degree_less:
                        tmp=tmp*0.75
                        continue
                    elif seg_result[i-j] in degree_least:
                        tmp=tmp*0.5
                        continue
            neg_score+=tmp
    
    sentiment_score=pos_score-neg_score
#    如果橘子最后有叹号
    if  seg_result[-1]=='!':
        sentiment_score*=1.5
    return sentiment_score    
                           
                        
#输出单条弹幕情感分析结果                        
def sentiment_result(sentence):                

    sentence=danmu_clean(sentence)
#    特殊处理两种情况
    if sentence=='???':
#        print('负面')
        jieba_res=-1
        ltp_res=-1
        return (jieba_res,ltp_res)  
    if sentence=='!!!':
#        print('正面')
        jieba_res=1
        ltp_res=1
        return (jieba_res,ltp_res)  
    if len(sentence)==0 or sentence==',' or sentence=='.':
#        print('中性')
        jieba_res=0
        ltp_res=0
        return (jieba_res,ltp_res)  
    
    
    jieba_list=jieba_word(sentence)
    ltp_list=ltp_word(sentence)
    
#    print('jieba_list:',jieba_list)
#    print('ltp_list:',ltp_list)
    
    sentiment_jieba=sentence_score(jieba_list)
    sentiment_ltp=sentence_score(ltp_list)
    
#    if sentiment_jieba>0:
#        print('jieba:','socre',sentiment_jieba,'class','正面')
#    elif sentiment_jieba<0:
#        print('jieba:','socre',sentiment_jieba,'class','负面')
#    else:
#        print('jieba:','socre',sentiment_jieba,'class','中性')
#        
#    if sentiment_ltp>0:
#        print('ltp:','socre',sentiment_ltp,'class','正面')
#    elif sentiment_ltp<0:
#        print('ltp:','socre',sentiment_ltp,'class','负面')
#    else:
#        print('ltp:','socre',sentiment_ltp,'class','中性')    
    
    if sentiment_jieba>0:
        jieba_res=1
    elif sentiment_jieba<0:
        jieba_res=-1
    else:
        jieba_res=0
        
    if sentiment_ltp>0:
        ltp_res=1
    elif sentiment_ltp<0:
        ltp_res=-1
    else:
        ltp_res=0
    
    return (jieba_res,ltp_res)    

#按时间段判断情感
def sentiment_fragment(sentiment_score_list):
    avg=sum(sentiment_score_list)/len(sentiment_score_list)
    return avg



#❤️
#❤ 这两种红心不一样   
#sentence="❤️"
#i,j=sentiment_result(sentence)
#print(i,j)
    
test_data=pd.read_csv(r'../data/test300.csv')
print('测试数量：',len(test_data))
jieba_flag=[]
ltp_flag=[]
start_time=time.clock()
for index,row in test_data.iterrows():
    danmu=str(row['danmu'])
    jieba_res,ltp_res=sentiment_result(danmu)
#    print(jieba_res,ltp_res)
    jieba_flag.append(jieba_res)
    ltp_flag.append(ltp_res)
end_time=time.clock()
print('测试用时：',end_time-start_time)
test_data['jieba']=jieba_flag
test_data['ltp']=ltp_flag
test_data.to_csv(r'../data/test300_result.csv',index=None)


segmentor.release()    
    