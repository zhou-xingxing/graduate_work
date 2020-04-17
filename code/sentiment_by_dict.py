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
#sentence="完了 带尼玛节奏 满嘴跑火车 老干爹的两个大鹅 来了 赢了 萌神真的萌 就这 样的 太菜了 摧枯拉朽的力量 挡住了 挡到了 灵儿又长又直"
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

test_list=['哈哈哈', '你是真的秀', '哈哈哈', '香香带带什么铭文', '再瞅一个试试', '666', '你可真是个鬼才', '净化庆', '一直', '哈哈哈', '6什么6,都坐下,基本操作', '???', '呵呵', '哈哈哈', '哈哈哈', '网络重拳出击', '哈喽哈喽,昨天干嘛了', '哈哈哈', '笑死我了哈哈哈', '哈哈哈', '我感觉这边可以赢', '灵魂净化', '哈哈哈', '净化', '哈哈哈', '骚白很好不喜欢请不要伤害', '很不错666啊', '吓死孩子了', '你的嘴真的开过光', '慌死了', '林度在哪里直播', '你把你的精华给我交了', '哈哈哈', '哈哈哈', '笑死我了', '哈哈哈', '哈哈哈', '哈哈哈', '这鬼谷子有毒', '呆', '哈哈哈', 'lj', '哈哈哈', '吓死了', '哈哈哈', 'mua～', '哈哈哈', '这鬼谷子有毒', '吓你', '哈哈哈', '来了老弟', '哈哈哈', '喜欢你', '哈哈哈', '算你傻', '哈哈哈', '哈哈哈', '胖揍他', '太细了', '太难了太难了', '俊俊加油加油💪加油加油💪加油加油💪加油加油💪加油', '来来来', '哈哈哈', '干得漂亮', '哈哈哈', '被追着打😂😂😂', '净化空气', '哈哈哈', '哈哈哈', '白妹不怕,哈哈哈啊哈', '哈哈哈', '捞捞捞', '净化庆祝', '吓哭了', '哈哈哈或或或或或或或', '林度在哪里直播', '999999999', '真厉害', '别怕', '太难了太难了', '太难了', '净化空气', '哈哈哈白白委屈', '蝙蝠：敢吃我?你怕是没死过', '今天状态不错呀', '哈哈哈', '哈哈哈', '小学生心态,越不让干越作,贱', '哈哈哈', '哈哈哈', '哈哈哈', '今天状态不错呀', '不按套路出牌', '哈哈哈.可可爱爱的', '哈哈哈', '哈哈哈,你个小可爱', '哈哈哈', '哈哈哈', '哈哈哈', '没事,反正你被她吓死三次了', '哈哈哈', '666', '你真的秀', '❤❤❤', '你是真的秀', '哈哈哈', '\U0001f92d\U0001f92d\U0001f92d\U0001f92d', '打不死你,吓死你', '哈哈哈', '233', '哈哈哈', '呵呵', '他喵的', '666', '怕不怕', '夕阳666', '净化空气', '哈哈哈', '画质怎么这么差', '哈哈哈', '233', '哈哈哈 舒服了', '来来来', '化空气.', '哈哈哈', '这谁顶得住啊', '吓得按净化', '真厉害', '这个皮肤要拥有原皮肤才能拿 吗', '❤❤❤', '哈哈哈', '慌得一匹', '把孩子给吓坏了', '哈哈哈', '哈哈哈', '你想多了骚骚', '净化空气', '关键吓你效果太好了', '哈哈哈', '🤣🤣🤣🤣', '233', '你可真是个鬼才', '骚白宝宝别怕', '白煤,别怕', '来来来', '她喜欢你', '你要吓哭了嘛', '打他', '哈哈哈', '细啊', '瞧把孩子吓得', '上次谁说要赢就找队友吵架的', '吓哭了', '净化庆祝', '没事没事', '净化了个寂寞', '哈哈哈', '❤❤❤', '白哥', '更可怕的是一个发干得漂亮,一个说收到的', '尿下出来了', '可能他只是单纯的不会玩', '笑死我了哈哈哈', '❤❤❤', '被火舞打出阴影了', '老李', '玩死你', '哈哈哈 舒服了', '这不就跟你上把廉颇吓后羿一样么', '仪式太好', '加油,', '哈哈哈捞', '你是真的秀', '很不错666啊', '净化空气', '哈哈哈', '不怕不怕', '被追着打😂😂😂', '骚白一夜之间变老了', '捞', '么么哒', '她不敢', '哈哈哈', '捞', '哈哈哈', 'd', '可爱ớ ₃ờớ ₃ờớ ₃ờớ ₃ờớ ₃ờớ ₃ờớ ❤❤', '哈哈哈', '哈哈哈', '无敌', '你是真的很多废话', '吓尿了', '年轻', '哈哈哈被吓坏了', '他吓我', '火舞万多了', '笑死我了', '有意见吗', '笑死我了哈哈哈', '可能他不会', '可能没摁出来', '应该是没按出来吧?', '吓的起', '净化空气', '哈哈哈', '是对手不行', '虚晃一枪', '估计是看你经济太低了,不值钱', '不怕 抱抱', '233', '就针对你', '哈哈哈', '刚才换我可能真的1闪上来了', '哈哈哈搞笑哦哦', '恐吓流', '哈哈哈', '哈哈哈 舒服了', '233', '没闪', '吓死你', '火舞是黔之驴', '一看见火舞吓出了净化', '给主播换条裤子', '第一个拿的谁的人头', '哈哈哈啊哈哈哈', '这个关羽笑死我了', '谁玩射手,就吓下谁', '可能刚刚发现没有闪现而已', '你可真是个鬼才', '火舞是上把的', '高手过招 点到为止 哈哈哈', '也可能是没闪出去', '他不会', '为什么骚白和纯白都学会东北话了', '233', '哈哈哈', '.666', '小心秃顶', '心态崩了', '她没摁出来闪现', '哈哈哈', '看把孩子吓的', '主播有点东西哈', '哈哈哈', '摸摸毛,吓不着', '没事 不怕', '净化都用了', '哈哈哈', '手滑了,没点出来', '算个屁', '进化空气', '666', '❤❤❤', '铭文啥啊', '他可能知道你是骚白', '666', '哈哈哈', '净化空气', '这队友别打了', '净化空气 净化自己', '吓得腿软了', '宝宝别怕', '干', '被火舞杀怕了哈哈哈', '👀', '差点尿裤衩了', '自己吓自己', '哈哈哈,自己吓自己', '你可真是个鬼才', '塑梦?', '夕阳666', '哈哈哈']


avg,pos_avg,pos_pro,neg_avg,neg_pos=sentiment_fragment(test_list)
print(avg,pos_avg,pos_pro,neg_avg,neg_pos)    


segmentor.release()    
    