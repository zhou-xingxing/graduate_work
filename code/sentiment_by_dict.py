# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:46:50 2020

@author: lenovo
"""

#基于情感词典的情感分析
import jieba
import os
from pyltp import Segmentor



# 加载自定义词典
jieba.load_userdict(r'../dict/self_dict.txt')


LTP_DATA_DIR = r'..\ltp_data_v3.4.0\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, r"..\dict\self_dict.txt")  # 加载模型，第二个参数是您的外部词典文件路径

sentence="一无所有"
jieba_words = jieba.cut(sentence)
ltp_words = segmentor.segment(sentence)

print(list(jieba_words))
print(list(ltp_words))