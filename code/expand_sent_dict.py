# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 16:38:46 2020

@author: lenovo
"""
#扩展情感词典
import pandas as pd
import os
from pyltp import Postagger
import jieba.posseg as pseg

#合并两种分词工具的词频统计结果，并去除低频词
def merge_and_remove_by_freq():
    jieba=pd.read_csv(r'../data/freq_st_jieba_cleaned_room36252danmu_500000.csv',header=None)
    
    ltp=pd.read_csv(r'../data/freq_st_ltp_cleaned_room36252danmu_500000.csv',header=None)
    
    jieba_dele=[]
    ltp_dele=[]
    
    for index,row in jieba.iterrows():
        if row[1]<10:
            jieba_dele.append(index)
    
    for index,row in ltp.iterrows():
        if row[1]<10:
            ltp_dele.append(index)
#    print(len(jieba_dele),len(ltp_dele)) 
    
    jieba=jieba.drop(index=jieba_dele)
    ltp=ltp.drop(index=ltp_dele)
    candidate=jieba.append(ltp)

    candidate.columns=['word','freq']
    candidate.sort_values(by='freq',ascending=False,inplace=True)
    
    candidate.drop_duplicates(subset=['word'],keep='first',inplace=True)
    candidate.to_csv(r'../data/candidate_sentiment.csv',header=None,index=None)


#去除游戏术语和已知情感词
def remove_by_specword():
    game_word=pd.read_csv(r'../dict/game_word.txt',header=None)
    game_word=game_word[0].tolist()
    
    pos=pd.read_csv(r'../dict/self_positive_dict.txt',header=None)
    neg=pd.read_csv(r'../dict/self_negative_dict.txt',header=None)
    
    pos_list=pos[0].tolist()
    neg_list=neg[0].tolist()
    print(len(game_word),len(pos_list),len(neg_list))
    dele=[]
    candidate=pd.read_csv(r'../data/candidate_sentiment.csv',header=None)
    for index,row in candidate.iterrows():
        if row[0] in game_word or row[0] in pos_list or row[0] in neg_list:
            dele.append(index)
            
    candidate.drop(index=dele,inplace=True)    
    candidate.to_csv(r'../data/candidate_sentiment.csv',header=None,index=None)
  


#词性标注
def word_pos():
#ltp词性标注
    candidate=pd.read_csv(r'../data/candidate_sentiment.csv',header=None)
    can_word=candidate[0].tolist()
    # 新加一列存放词性
    candidate.insert(2,'ltp_pos',0)
    candidate.insert(3,'jieba_pos',0)
    candidate.columns=['word','freq','ltp_pos','jieba_pos']

    LTP_DATA_DIR = '../ltp_data_v3.4.0/ltp_data_v3.4.0'  # ltp模型目录的路径
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    
    
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型   
    postags = postagger.postag(can_word)  # 词性标注   
    postagger.release()  # 释放模型   
    postags=list(postags)
    candidate['ltp_pos']=postags
#jieba词性标注    
    
    jieba_pos=[]
    for index,row in candidate.iterrows():
        s=row['word']
        words=pseg.cut(s)
        pos=[]
        for w in words:
            pos.append(w.flag)
        pos=' '.join(pos)
        jieba_pos.append(pos)
    
    candidate['jieba_pos']=jieba_pos
#    添加表头
    candidate.to_csv(r'../data/candidate_sentiment.csv',index=None)
    
    
    
  
#根据词性筛选
def remove_by_wordclass():
    # 筛选形容词、动词、叹词、成语、常用语、略语、描述性词
    jieba_flag=['ag','a','ad','an','e','i','I','j','vg','v','vd','vn']
    ltp_flag=['a','b','e','i','j','v','z']
#注意有header
    candidate=pd.read_csv(r'../data/candidate_sentiment.csv')
#取交集
    new_candidate=[]
    for index,row in candidate.iterrows():
        if row['ltp_pos'] in ltp_flag:
    #         new_candidate.append(row['word'])
    #         continue
            jieba_pos=row['jieba_pos'].split()
            for i in jieba_pos:
                if i in jieba_flag:
                    new_candidate.append(row['word'])
                    break
    
    new_candidate={'word':new_candidate}
    new_candidate=pd.DataFrame(new_candidate)
    new_candidate.to_csv(r'../data/new_candidate.csv',header=None,index=None)

    