import csv, re, os, time
import pandas as pd
from langconv import *


# 弹幕数据清洗


# 文本替换
def symbol_replace(s):
    # 全部小写
    s = s.lower()
    # 中英文标点、全角半角转换
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）“”‘’、％＃＠＆１２３４５６７８９０',
        u',.!?[]()""\'\',%#@&1234567890')}
    s = s.translate(table)
    # 去除两端空格
    s = s.strip()
    return s


# test_str='"打韩信就是要各种卖队友和抢人头,不然后期就费了"'
# print(symbol_replace(test_str))

# 简繁体转换
def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line


# test_str=" sdas[],.2das 干繁体字"
# print(tradition2simple(test_str))
# 同义词
def sim_replace(s):
    s = re.sub('(2+33+)', '233', s)
    s = re.sub('(^6+$)', '666', s)
    s = re.sub('(666+)', '666', s)
    # 表示一种回应
    s = re.sub('(^1+$)', '111', s)
    s = re.sub('(^2+$)', '222', s)
    s = re.sub('(111+)', '111', s)
    s = re.sub('(222+)', '222', s)
    # 777在台湾地区和666相似
    s = re.sub('(^7+$)', '777', s)
    s = re.sub('(777+)', '777', s)
    # 好像表示很无聊的意思
    s = re.sub('(ooo+)', 'ooo', s)
    s = re.sub('(ggg+)', 'gg', s)
    s = re.sub('(e+mm+)', 'emm', s)
    s = re.sub('(hh+)', '哈哈哈', s)
    s = re.sub('(嗯+)', '嗯嗯', s)
    s = re.sub('(啧+)', '啧啧', s)
    s = re.sub('(呵+)', '呵呵', s)
    s = re.sub('(哦+)', '哦哦', s)
    s = re.sub('(额+)', '额额', s)
    s = re.sub('(嘿嘿+)', '嘿嘿', s)
    s = re.sub('(嘻嘻+)', '嘻嘻', s)
    s = re.sub('(我我+)', '我我我', s)
    s = re.sub('(呜呜+)', '呜呜呜', s)
    s = re.sub('(嘤嘤+)', '嘤嘤嘤', s)
    s = re.sub('(啊啊+)', '啊啊啊', s)
    s = re.sub('(略略+)', '略略略', s)
    s = re.sub('(啦啦+)', '啦啦啦', s)
    s = re.sub('(捞捞+)', '捞捞捞', s)
    s = re.sub('(飞飞飞+)', '飞飞飞', s)
    s = re.sub('(冲冲冲+)', '冲冲冲', s)
    s = re.sub('(上上上+)', '上上上', s)
    s = re.sub('(秀秀秀+)', '秀秀秀', s)
    s = re.sub('(恍恍惚惚)+', '哈哈哈', s)
    s = re.sub('(红红火火)+', '哈哈哈', s)
    s = re.sub('(哈哈+)', '哈哈哈', s)
    s = re.sub('(大气)+', '大气', s)
    s = re.sub('(加油)+', '加油', s)
    s = re.sub('(…+)', '...', s)

    s = re.sub('(\?+)', '?', s)
    s = re.sub('(!+)', '!', s)
#    只有单独存在的? !才有特殊含义
    s = re.sub('(^\?+$)', '???', s)
    s = re.sub('(^!+$)', '!!!', s)
    s = re.sub('(,,+)', '...', s)
    s = re.sub('(\.\.+)', '...', s)
    return s


#print(sim_replace('谢谢老板大气大气大气啊捞 捞捞'))


# 表情替换
def emoji_replace(s,emot_dict):
    # 斗鱼专属表情
    for i in emot_dict.keys():
        s = re.sub('emot:' + i, emot_dict[i], s)
#❤️
#❤ 这两种红心不一样 
    s = re.sub('(❤️)', '❤', s)
    s = re.sub('(😃😃😃+)', '😃😃😃', s)
    s = re.sub('(💩💩💩+)', '💩💩💩', s)
    s = re.sub('(🐷🐷🐷+)', '🐷🐷🐷', s)
    s = re.sub('(🐶🐶🐶+)', '🐶🐶🐶', s)
    s = re.sub('(😂😂😂+)', '😂😂😂', s)
    s = re.sub('(❤❤❤+)', '❤❤❤', s)
    s = re.sub('(🎉🎉🎉+)', '🎉🎉🎉', s)
    s = re.sub('(🤮🤮🤮+)', '🤮🤮🤮', s)
    s = re.sub('(🚀🚀🚀+)', '🚀🚀🚀', s)

    return s



# 开始处理
# 以此文件的处理比例估算，可以减少1%的数据
def run_data_clean(fin,fout):    

    # 如果存在已清洗文件则删除重建
    if  os.path.isfile(os.path.join(fout)):
        os.remove(fout)

    with open(r"./dict/dyemot.txt", 'r')as f:
        emot_dict = eval(f.read())
    print("打开：" + fin,"开始清洗")
    start_time = time.clock()
    with open(fin, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line in reader:
            line[2] = symbol_replace(line[2])
            if len(line[2]) == 0 or line[2] == ',' or line[2] == '.':
                continue
            else:
                line[2] = tradition2simple(line[2])
                line[2] = sim_replace(line[2])
                line[2] = emoji_replace(line[2],emot_dict)
            with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
    #            如果有逗号，会自动加引号
                writer = csv.writer(nf)
                writer.writerow(line)
    end_time = time.clock()
    print("清洗结束：" + fout)
    print("清洗时间：" + str(end_time - start_time))
# 50W 394s 497441/500000=99.5%
# 23W 188s 
# 14w 114s
# 2W 17s


# 按每分钟对弹幕进行聚合
def danmu_60s_frag(fin, fout):
# 2W 0.7s
    print('打开：', fin,'开始聚合')
    start_time=time.clock()
    day1 = pd.read_csv(fin, header=None)
    day1.columns = ['id', 'time', 'danmu']
    day1["time"] = pd.to_datetime(day1.time.values, unit="s", utc=True).tz_convert('Asia/Shanghai').strftime(
        "%Y-%m-%d %H:%M")
    # 防刷屏处理
    day1 = day1.drop_duplicates(subset=['id', 'time', 'danmu'])
    time_group = day1.groupby('time')
    # print(time_group.size().describe())
    # 数量限制
    time_list = []
    danmu_list = []
    num_list = []
    for gn, gl in time_group:
        num = len(gl)
        # 数量少于30片段不分析
        # if  num <30:
        #     continue
        time_list.append(gn)
        num_list.append(num)
        danmu_list.append(gl['danmu'].tolist())
    dic = {'time': time_list, 'danmu': danmu_list, 'num': num_list}
    new_data = pd.DataFrame(dic)
    #    print(new_data)
    new_data.to_csv(fout, index=None)
    end_time=time.clock()
    print('按每分钟聚合文件：', fout)
    print('聚合时间',str(end_time-start_time))


if __name__=='__main__':
    # with open(r"../dict/dyemot.txt", 'r')as f:
    #     emot_dict = eval(f.read())
    #     print("表情符号字典加载完毕")
#    test_str = "[emot:dy101][emot:dy111]❤️❤❤❤🚀🚀🚀🚀🚀🚀❤💩💩💩💩💩💩🎉🎉🎉🎉🎉🎉"
#    print(emoji_replace(test_str,emot_dict))
#     fin="../data/room911/room911danmu0209.csv"
#     fout="../data/room911/cleaned_room911danmu0209.csv"
    
    # run_data_clean(fin,fout)
    fin="./danmu_data/danmu_cleaned.csv"
    fout = "./danmu_data/danmu_cleaned_frag.csv"

    danmu_60s_frag(fin,fout)


