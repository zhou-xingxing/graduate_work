# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:46:50 2020

@author: lenovo
"""

#基于词典的情感分析
import jieba
import os,time,csv
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
    
    score=pos_score-neg_score
#    print('score',score)
#    如果句子最后有叹号
    if  seg_result[-1]=='!':
        score*=1.5
    return score    
                           
                        
#输出单条弹幕情感分析结果                        
def sentiment_result(sentence):                

#    只有在测试单条弹幕时才需要清洗
#    sentence=danmu_clean(sentence)
#    特殊处理两种情况
    if sentence=='???':
#        print('负面')
        jieba_res=-1
        ltp_res=-1
#        return (jieba_res,ltp_res)  
        return jieba_res
    if sentence=='!!!':
#        print('正面')
        jieba_res=1
        ltp_res=1
#        return (jieba_res,ltp_res)  
        return jieba_res
    if len(sentence)==0 or sentence==',' or sentence=='.':
#        print('中性')
        jieba_res=0
        ltp_res=0
#        return (jieba_res,ltp_res) 
        return jieba_res
    
    
    jieba_list=jieba_word(sentence)
#    ltp_list=ltp_word(sentence)
#    
#    print('jieba_list:',jieba_list)
#    print('ltp_list:',ltp_list)
#    
    sentiment_jieba=sentence_score(jieba_list)
#    sentiment_ltp=sentence_score(ltp_list)
    
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
#    
#    if sentiment_jieba>0:
#        jieba_res=1
#    elif sentiment_jieba<0:
#        jieba_res=-1
#    else:
#        jieba_res=0
#        
#    if sentiment_ltp>0:
#        ltp_res=1
#    elif sentiment_ltp<0:
#        ltp_res=-1
#    else:
#        ltp_res=0
    
#    return (jieba_res,ltp_res)    
    return sentiment_jieba

#按时间段判断情感
def sentiment_fragment(danmu_list):
    sentiment_score_list=[]
    sentiment_pos_score=[]
    sentiment_neg_score=[]
    for i in danmu_list:
        score=sentiment_result(i)
        sentiment_score_list.append(score)
        if score>0:
            sentiment_pos_score.append(score)
        if score<0:
            sentiment_neg_score.append(score)
    num=len(sentiment_score_list)        
    avg=sum(sentiment_score_list)/num
#返回情感值累积和、平均值、正向和、负向和
#    return (sum(sentiment_score_list),avg,sum(sentiment_pos_score),sum(sentiment_neg_score))
#返回情感均值、正向情感均值、正向弹幕比
    return  (avg,sum(sentiment_pos_score)/num,len(sentiment_pos_score)/num)  



#❤️
#❤ 这两种红心不一样   
#sentence="好好好"
#i=sentiment_result(sentence)
#print(i)
#    
#测试弹幕
def test_danmu():    
    test_data=pd.read_csv(r'../data/test300_result_verify.csv')
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
    test_data.to_csv(r'../data/test300_result_verify.csv',index=None)
#
#测试时间段弹幕
def test_danmu_frag():
#    运行36秒
    data=pd.read_csv(r'../code/frag_cleaned_test_room911_20000.csv')
    time_group=data.groupby('fragment')    
    time_frag=[]
#    score_frag=[]
    avg_frag=[]
    pos_avg_frag=[]
    pos_pro_frag=[]
#    pos_frag=[]
#    neg_frag=[]
    start_time=time.clock()
    for gn,gl in time_group:
#        以每组第一条弹幕时间为坐标值
        time_frag.append(gl['time'].tolist()[0])
        avg,pos_avg,pos_pro=sentiment_fragment(gl['content'].tolist())
        
        avg_frag.append(avg)
        pos_avg_frag.append(pos_avg)
        pos_pro_frag.append(pos_pro)
    end_time=time.clock()
    print('测试用时：',end_time-start_time)
    dic={'time_frag':time_frag,'avg_score':avg_frag,'pos_avg':pos_avg_frag,'pos_proportion':pos_pro_frag}
    senti_frag=pd.DataFrame(dic)
    senti_frag.to_csv(r'../code/new2_senti_frag_cleaned_test_room911_20000.csv',index=None)

#test_danmu_frag()

#为时间段加特征
def feature_danmu_frag():
#    200s
    data=pd.read_csv(r'../data/hasflag_final_room36252danmu0318.csv') 
    avg_ls=[]
    pos_avg_ls=[]
    pos_prop_ls=[]
    start_time=time.clock()
    for index,row in data.iterrows():
#        print(row['danmu'],type(row['danmu']))
        avg,pos_avg,pos_prop=sentiment_fragment(eval(row['danmu']))
        
        avg_ls.append(avg)
        pos_avg_ls.append(pos_avg)
        pos_prop_ls.append(pos_prop)
    
    end_time=time.clock()
    print('测试用时：',end_time-start_time)
    data['avg_score']=avg_ls
    data['pos_avg_score']=pos_avg_ls
    data['pos_proportion']=pos_prop_ls
    
    data.to_csv(r'../data/hasflagfeature_final_room36252danmu0318.csv',index=None)
    
#    fin = "../data/hasflag_final_room36252danmu0318.csv"
#    fout = "../data/hasflagfeature_final_room36252danmu0318.csv"
#    print("打开：" + fin)
#    start_time = time.clock()
#    with open(fin, 'r', encoding='utf-8') as f:
#        reader = csv.reader(f)
#        for line in reader:
#            line[2] = symbol_replace(line[2])
#            if len(line[2]) == 0 or line[2] == ',' or line[2] == '.':
#                continue
#            else:
#                line[2] = tradition2simple(line[2])
#                line[2] = sim_replace(line[2])
#                line[2] = emoji_replace(line[2])
#            with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
#    #            如果有逗号，会自动加引号
#                writer = csv.writer(nf)
#                writer.writerow(line)
#    end_time = time.clock()
#    print("处理结束：" + fout)
#    print("处理时间：" + str(end_time - start_time))
    
    
        
#feature_danmu_frag()
    
test_list=['眼镜', '电线杆是啥', '谢谢办卡', '葛大爷', '???', '???', '你能不能早点奥日啊', '哈哈哈', '666', 'fly上', '刺痛好了吗', '嗯嗯?', '你眼睛去哪了', 'ag加油,ag加油', '???', '噗', '???', '我呵呵你', '???', '哈哈哈', '国服第一?哈哈哈', '什么第一', '???', '巅峰吧!我的快乐源泉', '???', '???', '???', '国服?', '大家为啥都喜欢奥日', '打到12点怎么办', '???', '国服第几?', '???', '???', '注意眼睛啊葛大爷', '国?', '哈哈哈', '???', '???', '???', '???', '你?', '???', '???', '???', '???', '???', '什么第一?', '梦里啥都有', '什么英雄', '国服哈哈哈', '奥日是啥', '???', '???', '你闹呢?', '国服?', '倒数第一?', '说的跟真的似的', '???', '敢不敢睁开眼说话', '醒醒', '痛痛好了', '?.?', '还没醒?', '别说梦话', '???', '???', '就你?', '你膨胀了', '???', '???', '国服第一?', '?什么', '国一扁鹊', '大可不必', '喝了几杯?', '???', '国一演员', '???', '几个菜,喝成这样', '醒醒?', '???', '竞猜', '你在逗我', '???', '白日梦', '国服扁鹊?', '???', '扁鹊吧', '?你?', '卡了?', '???', '现在还没到晚上', '我来晚了', '.?', '竞猜', '???', '几个菜啊', '...?', '搞得跟真的一样', '刺痛家旁边电线杆子被撞是真的吗?', '???', '哪个英雄', '国服倒数第一吗', '国服第一.?我没听错', '国服第一扁鹊?', '???', '梦里面什么都有?', '飞牛的冠军皮肤什么时候出?', '这么早', '???', '醒醒', '???', '小问号', '国服扁鹊', '???', '太难了太难了', '国服扁鹊?', '哪个国服', '大型问号现场', '但凡有粒花生米', '真的好了吗', '倒数第一?', '国服倒第一?', '醉成这样', '???', '咋闭眼了', '扁鹊嘛', '你改行直播奥日吧', '???', '醒醒', '赞一下?朋友们', '国服演员', '电线杆子好了吗', '扁鹊', '国服第一非你莫属', '刺痛怎么样了', '目标也不能不切实际啊', '我笑了', '???', '扁鹊吗', '星光荡开宇宙  fly闪耀其中', '小奶妈／?', '鹅鹅鹅鹅鹅', '不信', '葛大爷今天好早啊', '第一扁鹊?', '你早了一个小时,我网课还没上完你', '国服第一摇', '扁鹊还要冲吗?', '乔戈里峰', '国服第一扁鹊', '醒醒', '我是今天直播间签到第666名,给我点个赞吧~', '大白天做什么梦', '痛痛的网络好了么', '国服扁鹊', '已经是国服第一扁鹊了啊', '咋睡过去了?', '发一下首发名单', '哈哈哈', '国服第一扁鹊吗', '昨晚几斤', '国服倒一', '刺痛怎么了?', 'hurt家网还健在嘛', '刺痛今晚还能上吗', '[666]', '哈哈哈', '什么英雄?', '达摩', '只有目标没有实力哈哈哈', '扁鹊倒是稳了', '几个菜?', '好神奇的东西', '倒数第一', '国服第一啥啊', '国服第一扁鹊?', '但凡多几粒花生米', '为什么现在领不到40鱼丸了', '好的  人要有梦想[点赞]', '今天那么早', '越得不到越想要呗', '大中午喝多了', '痛痛的电线杆子修好了吗', '明天比赛几点开始,有谁知道', '太扯了', '哈哈哈', '倒数第一', '233', '优秀', '痛痛电线杆修好了吗锅锅', '笑死', '竞猜竞猜竞猜竞猜竞猜竞猜竞猜竞猜竞猜竞猜', '国服第一扁鹊', '国服扁鹊', '刺痛好了好了', '你那泡脚的呢', '竞猜在哪啊']
avg,pos_avg,pos_pro=sentiment_fragment(test_list)
print(avg,pos_avg,pos_pro)    


segmentor.release()    
    