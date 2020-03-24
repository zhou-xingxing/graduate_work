# 统计分析
# （2）弹幕数量以及高频词随时间变化的分布、绘制弹幕词云

import matplotlib.pyplot as plt
import pandas as pd
from pyecharts import Bar,Page,Line,WordCloud
from collections import Counter



#按时间段统计弹幕数量
def danmu_time_num():
    df=pd.read_csv(r"../code/cleaned_test_room911_20000.csv")
    df.columns=['id','time','content']
    handle_time=lambda x: int(x)
    df["time"]=df["time"].apply(handle_time)
    df["time"]=pd.to_datetime(df.time.values,unit="s",utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d %H:%M")
    time_count=pd.Series(df.groupby("time").size())
    time_count.to_csv(r"../code/time_count.csv")

#按时间段聚合弹幕分词
def danmu_time_word():
    # 注意去停用词后，csv没有header了
    df=pd.read_csv(r"../code/st_ltp_separate_cleaned_test_room911_20000.csv",header=None)
    df.columns=['id','time','content']
    handle_time=lambda x: int(x)
    df["time"]=df["time"].apply(handle_time)
    df["time"]=pd.to_datetime(df.time.values,unit="s",utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d %H:%M")
    time_group=df.groupby('time')
    
    time_ls=[]
    word_ls=[]
    
    for gn,gl in time_group:
    #     print(gn)
        ls=gl['content'].tolist()
    #     print(ls)
        lstr=' '.join(ls)
        time_ls.append(gn)
        word_ls.append(lstr)
    #     print(lstr)
    dic={'time':time_ls,'word':word_ls}
    time_word=pd.DataFrame(dic)
    time_word.to_csv(r"../code/time_word.csv",header=None,index=None)    



#加载弹幕数量聚合数据
# danmu_num=pd.read_csv(r'time_count.csv',header=None)
# time_data=danmu_num[0].tolist()
# new_time_data=[]
#只保留时间
# for i in time_data:
#     i=i.split()[1]
#     new_time_data.append(i)
# num_data=danmu_num[1].tolist()

def draw_danmu_num(time_data,num_data):
    page = Page()
    bar = Bar("弹幕数量分布图","2020-01-27",title_color='black', title_pos='center',width=1000)
    bar.add("弹幕数量", time_data, num_data, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(bar)
    
    line = Line("弹幕数量分布图","2020-01-27",title_color='black', title_pos='center',width=1000)
    line.add("弹幕数量", time_data, num_data, mark_line=['average'],mark_point=['max','min'],legend_pos='right',is_more_utils=True)
    page.add(line)
    page.render("danmu_num.html")
    
        
#draw_danmu_num(new_time_data,num_data)    
    
    
    



def cal_danmu_freq():
    #加载弹幕分词聚合数据
    time_word=pd.read_csv(r'../code/time_word.csv',header=None)
    time_word.columns=['time','word']
    words=time_word['word'].tolist()
    words=' '.join(words)
    words=words.split(' ')
    result = Counter(words) 
    # print(result.most_common(20))
    wd_ls=[]
    num_ls=[]
    for i,j in result.items():
        wd_ls.append(i)
        num_ls.append(j)
    # print(wd_ls)
       
    dic={'word':wd_ls,'num':num_ls}
    
    wd_fre=pd.DataFrame(dic)
    wd_fre=wd_fre.sort_values(by="num",ascending= False)
    
    # 删除频率小于某一值
    dele=[]
    for index,row in wd_fre.iterrows():
        if row['num']<100:
            dele.append(index)
       
    wd_fre=wd_fre.drop(index=dele)
    return wd_fre['word'].tolist(),wd_fre['num'].tolist()



def draw_danmu_wordcloud(word,freq):
   page=Page()
   wordcloud = WordCloud("弹幕词云图","2020-01-27 18:50",title_color='black', title_pos='center',width=1000,height=800)
   wordcloud.add("", word[:50], freq[:50], word_size_range=[45, 90],shape='diamond',word_gap=50,is_more_utils=True)
   page.add(wordcloud)
   page.render("danmu_word.html")


#加载词频数据
word,freq=cal_danmu_freq()

draw_danmu_wordcloud(word,freq)   
    
    
    
    