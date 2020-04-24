# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:06:26 2020

@author: lenovo
"""

#高光时刻分析
import pandas as pd
import numpy as np
from pyecharts import Bar,Page,Line,WordCloud,Pie

#可视化部分-折线图、饼图

def draw_senti(time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,fout):
#    数据预处理
    senti_sum=np.multiply(np.array(num),np.array(avg)).tolist()
    pos_sum=np.multiply(np.array(num),np.array(pos_avg)).tolist()
    neg_sum=np.multiply(np.array(num),np.array(neg_avg)).tolist()
    
    neg_sum=[i*-1 for i in neg_sum]
    neg_avg=[i*-1 for i in neg_avg]
    
#    不同倾向弹幕比例
    pos_num=np.multiply(np.array(num),np.array(pos_prop)).tolist()
    pos_num=np.rint(pos_num)
    neg_num=np.multiply(np.array(num),np.array(neg_prop)).tolist()
    neg_num=np.rint(neg_num)
    
    all_pos_prop=sum(pos_num)/sum(num)
    all_neg_prop=sum(neg_num)/sum(num)
    all_mid_prop=1-all_neg_prop-all_pos_prop
    senti_kinds=['正面','中性','负面']
    senti_prop=[all_pos_prop,all_mid_prop,all_neg_prop]
    
    page = Page()
    
    pie = Pie("各类弹幕占比","",title_color='black', title_pos='center',width=1600)
    pie.add("各类弹幕占比",senti_kinds, senti_prop, is_label_show=True,legend_pos='right')
    page.add(pie)
    
    bar = Bar("弹幕数量","",title_color='black', title_pos='center',width=1600)
    bar.add("弹幕数量", time, num, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("正面弹幕数量","",title_color='black', title_pos='center',width=1600)
    bar.add("正面弹幕数量", time, pos_num, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("负面弹幕数量","",title_color='black', title_pos='center',width=1600)
    bar.add("负面弹幕数量", time, neg_num, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("弹幕情感值","",title_color='black', title_pos='center',width=1600)
    bar.add("弹幕情感值", time, senti_sum, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("弹幕情感均值","",title_color='black', title_pos='center',width=1600)
    bar.add("弹幕情感均值", time, avg, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("正面弹幕情感值","",title_color='black', title_pos='center',width=1600)
    bar.add("正面弹幕情感值", time, pos_sum, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("正面弹幕情感均值","",title_color='black', title_pos='center',width=1600)
    bar.add("正面弹幕情感均值", time, pos_avg, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("负面弹幕情感值","",title_color='black', title_pos='center',width=1600)
    bar.add("负面弹幕情感值", time, neg_sum, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    bar = Bar("负面弹幕情感均值","",title_color='black', title_pos='center',width=1600)
    bar.add("负面弹幕情感均值", time, neg_avg, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    page.render(fout)
    print('echarts：',fout)
    
draw_fout="room911danmu0209.html"

data=pd.read_csv(r'../data/room911/senti_feature_frag_room911danmu0209.csv') 
time=data['time'].tolist()
num=data['num'].tolist()
avg=data['avg_score'].tolist()
pos_avg=data['pos_avg_score'].tolist()
neg_avg=data['neg_avg_score'].tolist()
pos_prop=data['pos_proportion'].tolist()
neg_prop=data['neg_proportion'].tolist()

draw_senti(time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,draw_fout)
    