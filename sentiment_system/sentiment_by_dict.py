# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:46:50 2020

@author: lenovo
"""

# 基于词典的情感分析
import jieba,os, time
from data_cleaning import sim_replace, symbol_replace, emoji_replace, tradition2simple
from langconv import *
import pandas as pd
import numpy as np
import joblib


# 加载自定义词典
jieba.load_userdict(r'./dict/self_dict.txt')
print("加载分词词典完毕")

pos_dict = pd.read_csv(r'./dict/self_positive_dict.txt', header=None)
pos_dict = pos_dict[0].tolist()

neg_dict = pd.read_csv(r'./dict/self_negative_dict.txt', header=None)
neg_dict = neg_dict[0].tolist()

not_dict = pd.read_csv(r'./dict/self_not.txt', header=None)
not_dict = not_dict[0].tolist()

with open("./dict/self_degree.txt", 'r', encoding='utf-8') as f:
    degree = eval(f.read())  # 把字典转化为str

degree_most = degree['most']
degree_more = degree['more']
degree_less = degree['less']
degree_least = degree['least']

print('正面情感词:', len(pos_dict))
print('负面情感词:', len(neg_dict))
print('否定词:', len(not_dict))
print('程度副词:', len(degree_most), len(degree_more), len(degree_less), len(degree_least))

with open(r"./dict/dyemot.txt", 'r')as f:
    emot_dict = eval(f.read())


# 数据清洗
def danmu_clean(sentence):
    sentence = symbol_replace(sentence)
    sentence = tradition2simple(sentence)
    sentence = sim_replace(sentence)
    sentence = emoji_replace(sentence, emot_dict)

    return sentence


# jieba分词
def jieba_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    # 去多余空格
    for i in seg_list:
        if i == ' ':
            continue
        else:
            seg_result.append(i)

    return seg_result


# 计算情感得分
def sentence_score(seg_result):
    pos_score = 0
    neg_score = 0

    for i in range(0, len(seg_result)):
        if seg_result[i] in pos_dict:
            # print('pos:', seg_result[i])
            tmp = 1
            # 向前查1-2个词
            for j in [1, 2]:
                if i - j < 0:
                    break
                # 有标点说明前后无联系，提前结束
                if seg_result[i - j] == ',' or seg_result[i - j] == '.':
                    break
                else:
                    if seg_result[i - j] in not_dict:
                        tmp = tmp * -1
                        continue
                    elif seg_result[i - j] in degree_most:
                        tmp = tmp * 1.75
                        continue
                    elif seg_result[i - j] in degree_more:
                        tmp = tmp * 1.5
                        continue
                    elif seg_result[i - j] in degree_less:
                        tmp = tmp * 0.75
                        continue
                    elif seg_result[i - j] in degree_least:
                        tmp = tmp * 0.5
                        continue
            pos_score += tmp
        elif seg_result[i] in neg_dict:
            # print('neg:', seg_result[i])
            tmp = 1
            # 向前查1-2个词
            for j in [1, 2]:
                if i - j < 0:
                    break
                if seg_result[i - j] == ',' or seg_result[i - j] == '.':
                    break
                else:
                    if seg_result[i - j] in not_dict:
                        # 负面词被否定词修饰视为无情感或略微正向
                        tmp = tmp * 0
                        continue
                    elif seg_result[i - j] in degree_most:
                        tmp = tmp * 1.75
                        continue
                    elif seg_result[i - j] in degree_more:
                        tmp = tmp * 1.5
                        continue
                    elif seg_result[i - j] in degree_less:
                        tmp = tmp * 0.75
                        continue
                    elif seg_result[i - j] in degree_least:
                        tmp = tmp * 0.5
                        continue
            neg_score += tmp

    score = pos_score - neg_score
    # print('score',score)
    # 如果句子最后有叹号
    if seg_result[-1] == '!':
        score *= 1.5
    return score


# 输出单条弹幕情感分析结果
def sentiment_single_result(sentence):
    # 只有在测试单条弹幕时才需要清洗
    sentence = danmu_clean(sentence)
    # 特殊处理两种情况
    if sentence == '???':
        # print('负面')
        jieba_res = -1
        return jieba_res
    if sentence == '!!!':
        # print('正面')
        jieba_res = 1
        return jieba_res
    if len(sentence) == 0 or sentence == ',' or sentence == '.':
        # print('中性')
        jieba_res = 0

        return jieba_res

    jieba_list = jieba_word(sentence)
    print('jieba_list:', jieba_list)
    sentiment_jieba = sentence_score(jieba_list)

    return sentiment_jieba


# 输出单条弹幕情感分析结果--为片段加特征用
def sentiment_single_result2(sentence):
    # 只有在测试单条弹幕时才需要清洗
    # sentence = danmu_clean(sentence)
    # 特殊处理两种情况
    if sentence == '???':
        # print('负面')
        jieba_res = -1
        return jieba_res
    if sentence == '!!!':
        # print('正面')
        jieba_res = 1
        return jieba_res
    if len(sentence) == 0 or sentence == ',' or sentence == '.':
        # print('中性')
        jieba_res = 0

        return jieba_res

    jieba_list = jieba_word(sentence)
    # print('jieba_list:', jieba_list)
    sentiment_jieba = sentence_score(jieba_list)

    return sentiment_jieba


# 为时间段提取特征
def sentiment_fragment(danmu_list):
    sentiment_score_list = []
    sentiment_pos_score = []
    sentiment_neg_score = []
    for i in danmu_list:
        score = sentiment_single_result2(i)
        sentiment_score_list.append(score)
        if score > 0:
            sentiment_pos_score.append(score)
        if score < 0:
            sentiment_neg_score.append(score)
    num = len(sentiment_score_list)
    avg = sum(sentiment_score_list) / num

    # 返回情感均值、正面情感均值、正面弹幕比、负面情感均值、负面弹幕比
    return (avg, sum(sentiment_pos_score) / num, len(sentiment_pos_score) / num, sum(sentiment_neg_score) / num,
            len(sentiment_neg_score) / num)


# 为弹幕文件加特征
def feature_danmu_frag(fin, fout):
    # 380 170-180s
    # 41 16s
    data = pd.read_csv(fin)
    print('打开文件：', fin)
    avg_ls = []
    pos_avg_ls = []
    pos_prop_ls = []
    neg_avg_ls = []
    neg_prop_ls = []
    start_time = time.clock()
    for index, row in data.iterrows():
        avg, pos_avg, pos_prop, neg_avg, neg_prop = sentiment_fragment(eval(row['danmu']))
        avg_ls.append(avg)
        pos_avg_ls.append(pos_avg)
        pos_prop_ls.append(pos_prop)
        neg_avg_ls.append(neg_avg)
        neg_prop_ls.append(neg_prop)

    end_time = time.clock()
    print('测试用时：', end_time - start_time)
    data['avg_score'] = avg_ls
    data['pos_avg_score'] = pos_avg_ls
    data['pos_proportion'] = pos_prop_ls
    data['neg_avg_score'] = neg_avg_ls
    data['neg_proportion'] = neg_prop_ls

    data.to_csv(fout, index=None)
    print('输出特征文件：', fout)

# 用机器学习模型预测情感倾向
def svm_model_test(fin, fout):
    data = pd.read_csv(fin)

    model_save_path = r"./model_save/"
    save_path_name = model_save_path + "svm_" + "train_model.model"
    svm_clf = joblib.load(save_path_name)

    feature = data.iloc[:, 2:8]
    # 标准化
    feature['num'] = (feature['num'] - feature['num'].mean()) / (feature['num'].std())
    X = np.array(feature)
    label = svm_clf.predict(X)
    data['predict'] = label
    data.to_csv(fout, index=None)
    print('利用模型预测情感倾向：', fout)


if __name__=='__main__':
    fin="./danmu_data/danmu_cleaned_frag.csv"
    fout="./danmu_data/danmu_cleaned_frag_feature.csv"
    # feature_danmu_frag(fin,fout)

    svm_model_test(fout,fout)