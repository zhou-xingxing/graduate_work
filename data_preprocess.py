# 二、预处理
# （1）增加自定义词典、分词、去除停用词（助词、虚词、介词）、词性标注。
# （结巴分词）（中科院分词系统）（哈工大ltp）
# 自定义词典：网络用语、专业术语、弹幕用语


import csv, os, re, time
import pandas as pd


# 合并、去重
def merge_dict(f1, f2, target):
    data1 = pd.read_csv(f1, header=None, encoding='utf-8')
    data2 = pd.read_csv(f2, header=None, encoding='utf-8')
    data1 = data1.append(data2)
    ans = data1.drop_duplicates()
    ans.to_csv(target, header=None, index=None)
    print("合并完成：", str(target))
    return


# f1=r"E:\毕业设计\弹幕新词记录.txt"
# f2=r"E:\毕业设计\词库\王者\wangzhe.txt"
# f2=r"E:\毕业设计\self_dict.txt"
# target=r"E:\毕业设计\self_dict.txt"
# merge_dict(f1,f2,target)

#加载停用词
st = open(r"../dict/stopwords.txt", encoding='utf-8-sig', errors='ignore')
stopwords = [' ']  # 增加空格
for line in st:
    line = line.strip()
    stopwords.append(line)
st.close()
print("停用词表构造完毕")
#print(stopwords)



# import jieba
# 加载自定义词典
# jieba.load_userdict(r'../self_dict.txt')
# 此种方法无效
# jieba.suggest_freq("???", tune=True)
# jieba.add_word('???', freq=20000)
# print("自定义词典加载完毕")


# 结巴分词
def jieba_separate_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = ""
    for i in seg_list:
        seg_result += i + ' '
    # 去多余空格
    ans = " ".join(seg_result.split())
    return ans


# jieba分不出 ??? !!!
# print(jieba_separate_word(sentence))

# fin="cleaned_test_room911_20000.csv"
# fout="jieba_separate_cleaned_test_room911_20000.csv"
#
# print("打开：" + fin)
# start_time = time.clock()
# with open(fin, 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for line in reader:
#         line[2] = jieba_separate_word(line[2])
#         with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
#             writer = csv.writer(nf)
#             writer.writerow(line)
# end_time = time.clock()
# print("处理结束：" + fout)
# print("处理时间：" + str(end_time - start_time))
# jieba 12-13s

# 哈工大LTP分词 路径不能有中文
LTP_DATA_DIR = r'..\ltp_data_v3.4.0\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
from pyltp import Segmentor

segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, r"..\dict\self_dict.txt")  # 加载模型，第二个参数是您的外部词典文件路径


def ltp_separate_word(sentence):
    # 自动去除多余空格
    words = segmentor.segment(sentence)
    new_words=[]
#    先把逗号去掉，不然写入csv时会自动加引号
#    for i in words:
#        if i==',':
#            continue
#        else:
#            new_words.append(i)
#    去停用词
    for i in words:
        if i in stopwords:
            continue
        else:
            new_words.append(i)
#    ans = ' '.join(words)
    ans = ' '.join(new_words)
    return ans


# 只有结尾的!!!会分开
#print(ltp_separate_word('"fuck shit , 要 身份证 啊 , 他们 能 去 吗"'))


fin="cleaned_test_room911_20000.csv"
fout="st_ltp_separate_cleaned_test_room911_20000.csv"
print("打开：" + fin)
start_time = time.clock()
# 去停用词，会把把第一行去掉
with open(fin, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for line in reader:
        line[2] = ltp_separate_word(line[2])
#        去空行
        if len(line[2])==0:
            continue
        with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
            writer = csv.writer(nf)
            writer.writerow(line)
end_time = time.clock()
print("处理结束：" + fout)
print("处理时间：" + str(end_time - start_time))
# ltp 13s 去停用词好像没有变慢？？+1s
segmentor.release()

# sentence="???熊大熊二吃屎啊???"
# 中科院分词-自己去掉结尾的语气词和多余的标点符号(... !!!) 细粒度最高 但某些情况下自己会删掉一些文本
# import pynlpir
# from pynlpir import nlpir
##from ctypes import c_char_p
# pynlpir.open()
# num=nlpir.ImportUserDict(b"..\self_dict.txt")
# print("加载自定义词典："+str(num))
def nlpir_separate_word(sentence):
    seg_list = pynlpir.segment(sentence, pos_tagging=False)
    seg_result = ""
    for i in seg_list:
        seg_result += i + ' '
    # 去多余空格
    ans = " ".join(seg_result.split())
    return ans
#
# fin="cleaned_test_room911_20000.csv"
# fout="nlpir_separate_cleaned_test_room911_20000.csv"
# print("打开：" + fin)
# start_time = time.clock()
# with open(fin, 'r', encoding='utf-8') as f:
#    reader = csv.reader(f)
#    for line in reader:
#        line[2] = nlpir_separate_word(line[2])
#        with open(fout, 'a', encoding='utf-8-sig', newline="") as nf:
#            writer = csv.writer(nf)
#            writer.writerow(line)
# end_time = time.clock()
# print("处理结束：" + fout)
# print("处理时间：" + str(end_time - start_time))
##nlpir 13s
# pynlpir.close()
