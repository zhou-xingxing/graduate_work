import csv, re, os, time
from langconv import *

# 弹幕数据清洗
# （1）去除无意义弹幕（比如只有一个./,）,过滤特殊字符（非字母数字文字表情）
# （2）对一些含义完全相同、表达存在细微差异的词（666+）作替换处理
# （3）英文字母全部小写、中英文标点符号转换、全角半角转换、简体替换繁体
#  (4) 常见表情符号、颜文字文本化

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


#test_str='"打韩信就是要各种卖队友和抢人头,不然后期就费了"'
#print(symbol_replace(test_str))

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
    s = re.sub('(111+)', '111', s)
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
    s = re.sub('(飞飞飞+)', '飞飞飞', s)
    s = re.sub('(冲冲冲+)', '冲冲冲', s)
    s = re.sub('(上上上+)', '上上上', s)
    s = re.sub('(秀秀秀+)', '秀秀秀', s)
    s = re.sub('(恍恍惚惚+)', '哈哈哈', s)
    s = re.sub('(红红火火+)', '哈哈哈', s)
    s = re.sub('(哈哈+)', '哈哈哈', s)
    s = re.sub('(…+)', '...', s)
    s = re.sub('(^\?+$)', '???', s)
    s = re.sub('(!+)', '!!!', s)
    s = re.sub('(,,+)', '...', s)
    s = re.sub('(\.\.+)', '...', s)
    return s


with open("dyemot.txt", 'r')as f:
    emot_dict = eval(f.read())
    print("表情符号字典加载完毕")


# 表情替换
def emoji_replace(s):
    # 斗鱼专属表情
    for i in emot_dict.keys():
        s = re.sub('emot:' + i, emot_dict[i], s)

    # s = re.sub('(😃)','[哈哈哈]',s)
    # s = re.sub('(💩)', '[大便]', s)
    # s = re.sub('(🐷)', '[猪头]', s)
    # s = re.sub('(🐶)', '[狗头]', s)
    # s = re.sub('(😂)', '[笑哭]', s)
    # s = re.sub('(❤)', '[红心]', s)
    return s


# test_str="[emot:dy101][emot:dy111]"
# print(emoji_replace(test_str))

# 开始处理
# 以此文件的处理比例估算，可以减少1%的数据
fin = "test_room911_20000.csv"
fout = "cleaned_test_room911_20000.csv"
print("打开：" + fin)
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
            line[2] = emoji_replace(line[2])
        with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
#            如果有逗号，会自动加引号
            writer = csv.writer(nf)
            writer.writerow(line)
end_time = time.clock()
print("处理结束：" + fout)
print("处理时间：" + str(end_time - start_time))
#16s
