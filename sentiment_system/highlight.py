# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:06:26 2020

@author: lenovo
"""

#高光时刻分析
import pandas as pd
import numpy as np
# from pyecharts import Bar,Page,Line,Pie

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
    

#加载已预测情感倾向的文件
def load_data(fin):
    data=pd.read_csv(fin)
#    print(len(data))
#    剔除数量小于30的片段，没有研究意义
    dele=[]
    for index,row in data.iterrows():
        if row['num']<30:
            dele.append(index)
    data.drop(index=dele,inplace=True)
    print('片段个数：',len(data))
    time=data['time'].tolist()
    num=data['num'].tolist()
    avg=data['avg_score'].tolist()
    pos_avg=data['pos_avg_score'].tolist()
    neg_avg=data['neg_avg_score'].tolist()
    pos_prop=data['pos_proportion'].tolist()
    neg_prop=data['neg_proportion'].tolist()
    senti_class=data['predict'].tolist()
    
    return time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,senti_class

def senti_report(time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,senti_class,fout):
    f=open(fout,'w',encoding='utf-8')
    print('弹幕片段情感分析报告',file=f)
#数量分析
    num_pd=pd.Series(num)
    num_avg=num_pd.mean()
    print('\n弹幕数量分布：',file=f)
    print(num_pd.describe(),file=f)
    
    #    不同倾向弹幕比例
    pos_num=np.multiply(np.array(num),np.array(pos_prop)).tolist()
    pos_num=np.rint(pos_num)
    neg_num=np.multiply(np.array(num),np.array(neg_prop)).tolist()
    neg_num=np.rint(neg_num)
    
    all_pos_prop=sum(pos_num)/sum(num)
    all_neg_prop=sum(neg_num)/sum(num)
    all_mid_prop=1-all_neg_prop-all_pos_prop
    
    print('\n正面弹幕数量：','{:.0f}'.format(sum(pos_num)),'占比：','{:.2%}'.format(all_pos_prop),file=f)
    print('中性弹幕数量：','{:.0f}'.format(sum(num)),'占比：','{:.2%}'.format(all_mid_prop),file=f)
    print('负面弹幕数量：','{:.0f}'.format(sum(neg_num)),'占比：','{:.2%}'.format(all_neg_prop),file=f)
    

    highlight_list=[]
    fight_list=[]
    storm_list=[] 
    negative_list=[]
    
    for i in range(len(time)):
        #   高光时刻 
        if num[i]>=num_avg and senti_class[i]==1:
            highlight_list.append(i)
        #   争议时刻
        if pos_prop[i]>=0.3 and neg_prop[i]>=0.3:
            fight_list.append(i)
        #   弹幕风暴
        if num[i]>=1000:
            storm_list.append(i)
        #   负面时刻
        if senti_class[i]==-1:
            negative_list.append(i)
    
    print('\n高光时刻：',str(len(highlight_list))+'个',file=f)
    for i in highlight_list:
        print(time[i],file=f)

    print('\n争议时刻：',str(len(fight_list))+'个',file=f)
    for i in fight_list:
        print(time[i],file=f)
                                    
    print('\n负面弹幕警告：',str(len(negative_list))+'个',file=f)
    for i in negative_list:
        print(time[i],file=f)

    print('\n弹幕风暴时刻：', str(len(storm_list)) + '个', file=f)
    for i in storm_list:
        if senti_class[i] == 1:
            print(time[i], '正面', file=f)
        if senti_class[i] == 0:
            print(time[i], '中性', file=f)
        if senti_class[i] == -1:
            print(time[i], '负面', file=f)

    f.close()
    print("报告生成完毕")
    

if __name__=='__main__':
    fin = r"E:/sentiment_system/frag_data/frag_file.csv"
    fout = r"E:/sentiment_system/frag_data/frag_report.txt"
    time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,senti_class=load_data(fin)
   # draw_fout="new_room911danmu0209.html"
   # draw_senti(time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,draw_fout)
    senti_report(time,num,avg,pos_avg,neg_avg,pos_prop,neg_prop,senti_class,fout)




    