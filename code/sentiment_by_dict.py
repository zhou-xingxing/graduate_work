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
            print('pos:',seg_result[i])
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
            print('neg:',seg_result[i])
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
    print('jieba_list:',jieba_list)
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
#sentence="完了 带尼玛节奏 满嘴跑火车 老干爹的两个大鹅 来了 赢了 萌神真的萌 就这 样的 太菜了"
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
#    170-180s
    data=pd.read_csv(r'../data/room36252/new_flagfeature_final_room36252danmu0318.csv') 
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
    
    data.to_csv(r'../data/room36252/new_flagfeature_final_room36252danmu0318.csv',index=None)
    
    
    
        
#feature_danmu_frag()

test_list=['可以的', '很清晰啊', '我66', '末将会', '很清晰了', '不道歉就能上场?', '好的好的', '你真的秀', '汉国汉国兄汉国兄汉国兄汉国兄汉国～～～～～～～～～', '可以了', '很清晰啊', '很清晰了', '肥牛腊鸡,不配做人', '今天状态不错呀', '小giao上位要成为峡谷最有钱的男人了', '老帅呢老帅呢老帅呢老帅呢老帅呢老帅呢老帅呢老帅呢老帅呢老帅呢', 'qg加油!', '赶紧好卡啊', '麟羽为什么没上', '不管你是谁,我就20分钟后', '看着挺清晰的', '关掉解说干嘛?', '很清楚', '很好了', '官方声音稍微有点大呢', '我害怕啊', '很清晰阿', '没事', '刺痛李白?', '要那么多要求', '很清楚了呀', '这画质属实一般', '官方小一点', '可以了', '不要刷屏', '真的吗4m', '很清楚', '官方声音关掉', '233', '花木兰会上吗', '盾山附魔', '你们有蓝光自己开', '很不错666啊', '可以了可以了', '可以了', '看不清的是自己么', '挺清楚的啊', '挺好的', '被虐哭了,请求大佬支援#挑战666#', '可以了', '很清楚', '一诺国服盾山', '可以了', '封盘', '挺清晰的啊', '选手的摄像头呢', '很清晰', 'ag更稳', 'qg冲', '站不了视野', '许诺和hurt,棒棒哒', '想听游戏声音', '哈哈哈 舒服了', 'fly冲冲冲', '我就是觉得很暗屏幕', '这是表演赛吗', '这是春季晒吗?', '刺痛家的网好了吗?', '牛牛玩了一个好重的英雄', '好紧张啊', '很清晰,可以了', '贼清楚', '官方那个瓶子明显偏心ag不想听', '自己可以调清晰度的', '游戏声音呢', '进来看到飞牛玩吕布?', '其实我想看巅峰赛', '老帅说了不会上场了', '老帅呢', '把官方解说关了', '我在#挑战666#中的成绩是6.65秒,是兄弟就来挑战666〉〉', '把他们的麦关了啊', '这谁顶得住啊', '很清晰  不清晰的擦擦手机屏幕', '飞牛腊鸡,不配做人!', '把解说的声音关掉', '这把最少20分', '666', '能不能把官方的声音调轻点啊', '很不错666啊', '抢到了', '驯龙高手不行了', '那个说老帅的自己去看微博', '游戏声音呢?', '刺痛不当厨师长了,要上菜了', '挺清楚', '超级凶', '我在#挑战666#中的成绩是6.66秒,是兄弟就来挑战666〉〉', '赛马', '路上的小小花都能看清', '666', '不急', '一诺打的非常一诺', '啥玩意啊?', '不应该拿李白呀', '小一诺太凶了', '把官方解说声音关掉吧不然太吵了', 'giao玩李白是演员', '一诺冲冲冲', '驯龙高手giao233', '听不见游戏声音', '好卡', 'giao还是蓝领野好点', '右上角有蓝光4m', '嗯嗯...', '嘻嘻', '李白!', '有没有赛程表 @a么么儿吖：不要刷屏', '诺崽冲冲冲', '老帅呢', '一诺打得非常一诺', '一诺打的非常一诺', '官方小点', '游戏声音有点小', '关解说', '❤❤❤', '官方太大了太杂了', '房管禁言啊', '前期不好打', '刺痛不是断网了吗', '官方声音能不要吗', '现场解说的声音轻一点', '加油', '吧官方的声音调小', '好惨', '没惩击 giao手也没办法', '自己看老帅微博去', '哈哈哈 舒服了', '把官方的声音关了吧', '关解说', '方法', '刺痛李白?', '啊啊啊', '刺痛李白?', '有内鬼', '用薪创造快乐.', '打不过', 'giao之前在练李白', '拿李白吃经济又打不出效果', '导播视角很难受啊', '不急不急', '李白!', '把官方解说的声音关掉', '我在#挑战666#中最好成绩是6.53秒,你能超越我吗?', '阿德', '不能关声音 要不然游戏声音没了', '关掉官方声音吧', '感觉是qg最喜欢的阵容了', "'", '对', '今天状态不错呀', '666', 'aluk', '这周有超级粉丝团的任务,欢迎超火飞机办卡荧光棒小礼物安排,谢谢大家!', 'sjy别看了', '关解说吧', 'giao：奖励自己一把李白', '年崽冲冲冲', '其实我想看巅峰赛', 'lmx我是你爸爸', '养猪双核', '不管了', '喜欢飞牛喜欢ag是真的难', '一诺打的好凶', '下反了', '这是表演赛吗', '什么鬼阵容?', '七年能上?', '炸了啊giao', 'qg', '黛打打的赢搞笑', '5秒真男人的时代已经过去,在这个直播间就来#挑战666#', '要听游戏声音啊', '李白被反野基本输', '张良打西施不好打', '关什么官方?要求那么多?', '可以的', '论人气ag就没输过', '不慌还没到20分钟']



avg,pos_avg,pos_pro,neg_avg,neg_pos=sentiment_fragment(test_list)
print(avg,pos_avg,pos_pro,neg_avg,neg_pos)    


segmentor.release()    
    