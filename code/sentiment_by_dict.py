# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:46:50 2020

@author: lenovo
"""

#基于词典的情感分析
import jieba
import os,time,csv
from pyltp import Segmentor
from data_cleaning import sim_replace,symbol_replace,emoji_replace,tradition2simple
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

with open(r"../dict/dyemot.txt", 'r')as f:
    emot_dict = eval(f.read())
#数据清洗
def danmu_clean(sentence):
    
        
    sentence=symbol_replace(sentence)
    sentence=tradition2simple(sentence)
    sentence=sim_replace(sentence)
    sentence=emoji_replace(sentence,emot_dict)
    
    return sentence


#test_str = "[emot:dy104][emot:dy111]❤️❤❤❤🚀🚀🚀🚀🚀🚀❤💩💩💩💩💩💩🎉🎉🎉🎉🎉🎉"
#print(danmu_clean(test_str))

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
    
    if sentiment_jieba>0:
        jieba_res=1
    elif sentiment_jieba<0:
        jieba_res=-1
    else:
        jieba_res=0
        
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
#返回情感均值、正面情感均值、正面弹幕比、负面情感均值、负面弹幕比
    return  (avg,sum(sentiment_pos_score)/num,len(sentiment_pos_score)/num,sum(sentiment_neg_score)/num,len(sentiment_neg_score)/num)  



#❤️
#❤ 这两种红心不一样   
#sentence="别骂了 不要脸 给你脸了 别给脸不要脸"
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
    test_data.to_csv(r'../data/new_test300_result_verify.csv',index=None)
    
#test_danmu()    
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
#   380 170-180s
    data=pd.read_csv(r'../data/room911/final_room911danmu0206.csv') 
    avg_ls=[]
    pos_avg_ls=[]
    pos_prop_ls=[]
    neg_avg_ls=[]
    neg_prop_ls=[]
    start_time=time.clock()
    for index,row in data.iterrows():
#        print(row['danmu'],type(row['danmu']))
        avg,pos_avg,pos_prop,neg_avg,neg_prop=sentiment_fragment(eval(row['danmu']))
        
        avg_ls.append(avg)
        pos_avg_ls.append(pos_avg)
        pos_prop_ls.append(pos_prop)
        neg_avg_ls.append(neg_avg)
        neg_prop_ls.append(neg_prop)
    
    end_time=time.clock()
    print('测试用时：',end_time-start_time)
    data['avg_score']=avg_ls
    data['pos_avg_score']=pos_avg_ls
    data['pos_proportion']=pos_prop_ls
    data['neg_avg_score']=neg_avg_ls
    data['neg_proportion']=neg_prop_ls
    
    data.to_csv(r'../data/room911/feature_final_room911danmu0206.csv',index=None)
    
    
    
        
#feature_danmu_frag()

#test_list=['不喜欢元歌,没有观赏性', '主播是真的顶', '骚白有个吉尼斯500连胜的', '一个人的逆风', '主播有点东西哈', '哈喽', '一个一技能,你就没了', '拔不掉高地你们10分钟后崩了', 'skr skr skr skr', '昨天怎么没有播呀', '白哥买个变声器开麦吧', '围绕他打是因为萌芽 傻吧', '噗', 'kk', '哈哈哈', '这谁顶得住啊', '干得漂亮', '@a病态恐怖：白哥买个变声器开麦吧 就你捞', '+++-----+---------------------', '哈哈哈', '飘了啊', '你说话小声点听不见队友', '你们没射手还敢打后期?', '666', '后期打不了', '❤❤❤', '主播是真的顶', '后期萌芽无敌了', '元歌还没观赏性?', '1433223', '这谁顶得住啊', '这一套?', '666', '很不错666啊', 'skr skr skr skr', '你真是个变脸比翻书还快的男人', '被追着打😂😂😂', '真厉害', '源哥太酷了', '太捞了', '666 99999999996699966996696696996996996969969699969966699999999666 666', '怎么又玩元歌', '666', '会个屁', '太难了太难了', '主播不要逗', '白哥心态崩了哈哈哈', '一个人的逆风', '❤❤❤', '666', '❤❤❤', '捞', '你是真的秀', '这是白哥玩的捞', '233', '他们永远不知道元歌是骚白', '你有本事单杀他呀', '666', '白妹', '❤❤❤', '怎么又是元哥', '真厉害', '对面李白送的', '😓😓😓', '看看专业源哥真秀', '真厉害', '变声器多好', '[喵喵][喵喵][喵喵][喵喵]', '香蕉味?还是草莓味?', '白妹你唠了', '白哥心态崩了哈哈哈', '哈哈哈', '233', '被追着打😂😂😂', '真厉害', 'jszrediyi', '666', '骚白申请交流', '------++++', '233', '萌娃后期输出爆炸😄😄😄', '今天刚学会了婉儿起飞.好开心很开心.', '嗯嗯?', '666', '他们永远不会知道元歌是骚白', '666', '你看看你战绩,你玩个什么东西', '药瓶a', '二娃是?', '@a云1来也：不喜欢元歌,没有观赏性', '😓😓😓', '好像是djie', '弱化打不动', '超喜欢元歌这个英雄', '呵呵', '就喜欢这样的你.', '白哥心态崩了哈哈哈', '唠', '再个鬼的见', '弱化', '???', '你又飘了', '庄周弱化', '他没被教育过', '笑死我了哈哈哈', '这谁顶得住啊', '开麦', '何止一点', '后期你们两法师：干将,李信,不可能打不过', '火舞真秀', '弱化啊', '太难了太难了', '哈哈哈', '六六六', '被追着打😂😂😂', '!!!', '确实再见', '呵呵', '瞎jb乱开', '笑死我了哈哈哈', '是你太秀', '讲道理,你元歌也就星耀水平', '开麦', '一点点', '哈哈哈', '开局你六神就赢定了', '你技能歪了', '再见', '白哥心态崩了哈哈哈', '再见,队友', '很大的问题', '就喜欢这样的你.', '哈哈哈', '牛皮', '弱化', '🈶弱化', '你low了', '被追着打😂😂😂', '被追着打😂😂😂', '33-', '你真的秀', '哈哈哈', '哈哈哈', '哥,我又来了', '加油', '被追着打😂😂😂', '哈哈哈 舒服了', '若华,现在剪上贼厉害', '混子', '一点点吗', '❤❤❤', '虚弱了', '切不到后排', '你没点用', '元哥的技能不太好看', '腊鸡', '弱化太强了', '不有弱化', '团灭发动机', '心理战', '配合不默契', '弱化', '主播有点东西哈', '梦飞的连胜是啥意思', '弱化了', '拽犯法吗,有哪条法律规定人不能拽的', '???', '白哥心态崩了哈哈哈', 'skr skr skr skr', '弱化', '开始抱大腿', 'll没事', '难受', '哈哈哈', '就喜欢这样的你.', '亿点点']
#
#
#avg,pos_avg,pos_pro,neg_avg,neg_pos=sentiment_fragment(test_list)
#print(avg,pos_avg,pos_pro,neg_avg,neg_pos)    


segmentor.release()    
    