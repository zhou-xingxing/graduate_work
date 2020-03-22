# 统计分析
# （2）弹幕数量以及高频词随时间变化的分布、绘制弹幕词云

import wordcloud
import matplotlib.pyplot as plt
import pandas as pd
# from pyecharts import Bar,Page,Line

# 设置背景图片用
# from PIL import Image
# import numpy as np

def draw_wordcloud(sentence):
    # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
    w = wordcloud.WordCloud(width=1000,
                            height=800,
                            background_color='white',
                            font_path='msyh.ttc',
                            scale=5,
                            max_words=50,
                        )

    wc=w.generate(sentence)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file('wordcloud.png')



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
    page.render("echarts.html")
    
        
#draw_danmu_num(new_time_data,num_data)    
    
    
    
#加载弹幕分词聚合数据
danmu_word=pd.read_csv(r'time_word.csv',header=None)
#print(danmu_word)
#随便选一分钟画一下
#print(danmu_word[1][0])
draw_wordcloud(danmu_word[1][2])    
    
    
    
    