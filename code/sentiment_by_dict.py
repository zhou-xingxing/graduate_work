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
#返回情感均值、正面情感均值、正面弹幕比、负面情感均值、负面弹幕比
    return  (avg,sum(sentiment_pos_score)/num,len(sentiment_pos_score)/num,sum(sentiment_neg_score)/num,len(sentiment_neg_score)/num)  



#❤️
#❤ 这两种红心不一样   
sentence="别喷了 搞笑 有点道理 有点牛 这他妈打的什么 有点水 水友 放水 我想喝水"
i=sentiment_result(sentence)
print(i)
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
#    180s
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

#test_list=['有道理呀', '许诺今天有点下饭', '我去', 'ag 3:0 qg不解释', '张飞一点意识没有  早大就可以了', '用薪创造快乐.', '张飞肯定以为可以直接杀啊', '我觉得770开团辅助玩的不好,但是张飞玩的比这个绝对强一点吧', '不想喷,辅助还是有问题', 'ag冲冲冲', '打野吧,让buff', 'qg买了最初?', '我要得一儿', '黑暴快哭了', 'qg辅助没一个好的', '可以可以', '张飞大狂铁闪换了一个黄忠闪', '为什么九分钟就有小龙', '没有大招的张飞没办法抢龙 所以想留', '谁能想到啊?', 'qg 加油', '喷许诺的事项上九月吗?', '太乙意识很好也', '带节奏的出去,没人叫你看', '马克经济多', '哔哔辅助干嘛', '你到底是那边的', '轻点喷,你们qg辅助少,喷走了就没了', '许诺以为fly能杀没问题啊啊啊', '这个不抢人头好不好', '玩过辅助?在这比比?', '哇', '刺痛争点气啊', '反着买,别墅靠海', '上帝视野牛逼?', '一动不动似王八', '233', '许诺就是snow', '哈哈哈啊哈哈哈', '一动不动似王八', '赫尔特的电线杆是你撞的吧', '我刚才也以为狂铁能杀啊,为什么要放大', '刺痛家没有网', '哈哈哈', '带节奏关你吊事,自己屏蔽弹幕', '马可经济好高', '太难了太难了', '开个弱化进去就能顶住', 'qg狗急了?', '人家愿意说,没办法 @awyj86985：许诺怎么了,喷子有病吧', '不要带节奏', '唉', '这把感觉qg要无了...', '别带许诺节奏.!', '没视野啊', '还以为曜驯龙高手', '所以为什么不买最初啊?', '末将按的好', '还是fly呀', '总是有些喷子喜欢乱喷 人在每一个主播的直播间里都会见到', '一个边路已经不错了', '哈哈哈', '最初是经济又实惠', '又无了', '哈哈哈', '那就是fly的问题呗', '黄忠起来了要怎么打', '我是真的不懂你们当初为什么不买最初', 'qg打得真气人啊', '有内鬼', 'qg谁在指挥?', 'qg', '然后就被开了', '有道理呀', '你真的秀', '无了啊', '一动不动是王八', 'giao之前在练李白', '我要得一儿', '哇', '别骂张飞 许诺比韭黄好太多了', '你那边的?', '毒奶', '...', '怎么打成这样了', '第二打野', '无了呀', '许诺永远滴神!', '一动不动似王八?', '许诺真的会玩吗', '无了', 'qg全员都很好', '这黄忠打人打得笑死我了', '很不错666啊', '黄忠破晓了啊', '按早了', '总是自己断节奏', '我要得一儿', '毒奶', '两队差距太大了', '开了自动攻击', '飞哥牛逼', '输了啊', '太难了太难了', '张飞以为狂铁最后那一下能打死黄忠,所以大开晚了', '黄忠没了...', '所以就是说是判断失误嘛', '不好打啊', '感觉黄忠cd好大', '刚来,问一下奶的谁', '啊啊啊', '毒奶降临', 'qg是不是没打过顺风啊', '我吐了.听你的压了qg', '哈哈哈', '有内鬼', '毒奶', '刺痛李白?', '毒奶哈哈哈', '线也差,龙也没,打毛', 'qg没了', '黄忠经济起来了', '辅助不行', '不会被零封吧', '无了呀', '还好我压的ag', '跟我念:qg这把不好打', '毒奶', '别带节奏', '打毛线', 'qga', '唉', '你出钱,人机ag先下手@a薄荷糖13248我就不懂你们为什', '❤❤❤', '啊啊啊', 'qg是真的菜啊', '你以为?  你牛逼你上?', '别喷了别喷了', '不看了', 'giao之前在练李白', '一动不动似王八', '切不到太难了', '带节奏还有理了?', '我刺痛也可以', '无了', '后裔能站撸黄忠', '可惜看不到基尼了', '为啥给牛拿吕布啊醉了', '要零封了', '指挥没思路', '年少转身拿蓝', '有道理呀', '王昭君打黄忠很好打啊', '国服扁鹊', '无人能近身', '输了啊', '别tm带节奏', 'qg加油', '怂  烦死了', '无了无了', '菜逼扣鸡🐔', '你咋这么逗乐呢', '买个纯净苍穹', '黛打打的赢搞笑', '又无了', '真:毒奶', '黄忠经济很高', '请问哪个射手现在不变态', '带许诺节奏的是想上韭黄🐎?', '毒奶是不是', '喷子又来了', '完了', 'bo几', '哈哈哈', '破产了', '两炮轰死一个c😂', 'qg不行,气死了', '老兵不老', '刺痛李白?', 'mua～', 'hurt加油!干他!', '梦奇可以打黄忠吗', '别奶了!', '许诺辅助不行', '起来就是黄三炮', '我感觉是狂铁的问题', '还好我压的ag', '好紧张', '上杰杰吧', '一直都认为许诺辅助一般', '破晓了很难顶', '司马懿虐杀', '婉儿偷袭可以', '黄忠经济可以的', '很不错666啊', '后羿已经没黄忠厉害了', '黄忠架炮距离太远没法头像锁定', '黄忠你被奶了,快死', '3比零结束呗?', '老夫子吊着打', 'skr skr skr skr', '怎么感觉又要无了', '黄7泡哈哈哈', '黄忠后期超猛', '❤❤❤', '嘻嘻', '喷许诺的是想上九月还是770?', '天天喷许诺,那上770九月吧,看你们是输是赢赖', 'giao不行打不了野核', '为什么qg玩黄忠没有这种感觉', '会换770吗', '鬼英雄哈哈哈', 'qg好菜啊', '还在大庄,按纯净苍穹', '慌的一b', '所以笑影以前叫汤汤吗', '无了呀', '毒奶', 'giao之前在练李白', '链接qg', '看得我心跳', '二营长把我的意大利炮拿来', '沟通问题 别说了', '我都说了qg帮3:0带走了', '要被零封了', '许诺总是断节奏啊', '这谁顶得住啊', 'qg怎么没那么厉害了', '黄忠的发育曲线很不线性', '又赔了', '为啥给牛拿吕布啊醉了', '毒奶', '暴君击杀ag哈哈哈', '别奶了']
#
#
#avg,pos_avg,pos_pro,neg_avg,neg_pos=sentiment_fragment(test_list)
#print(avg,pos_avg,pos_pro,neg_avg,neg_pos)    


segmentor.release()    
    