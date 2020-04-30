from flask import Flask, render_template, request, send_from_directory
from sentiment_by_dict import *
from data_cleaning import run_data_clean, danmu_60s_frag
import highlight

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# 自定义词典页面
@app.route('/dict_page')
def dict_page():
    return render_template("dict_page.html")


# 上传自定义词典并合并
@app.route('/user_dict_upload', methods=['POST'], strict_slashes=False)
def user_dict_upload():
    file_dir = 'E:/sentiment_system/user_dict'  # 文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    user_fenci = request.files['fenci_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    user_pos = request.files['pos_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    user_neg = request.files['neg_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(file_dir, user_fenci.filename, user_pos.filename, user_neg.filename)
    user_fenci_ans, user_pos_ans, user_neg_ans = False, False, False
    if user_fenci and '.' in user_fenci.filename and user_fenci.filename.rsplit('.', 1)[1] == 'txt':
        fname = user_fenci.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_fenci_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_fenci.save(os.path.join(file_dir, new_filename))
        user_fenci_ans = True
        user_fenci_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_fenci_dict = user_fenci_dict[0].tolist()
        print('用户自定义分词个数', len(user_fenci_dict))
        for i in user_fenci_dict:
            jieba.add_word(i)

    if user_pos and '.' in user_pos.filename and user_pos.filename.rsplit('.', 1)[1] == 'txt':
        fname = user_pos.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_pos_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_pos.save(os.path.join(file_dir, new_filename))
        user_pos_ans = True
        user_pos_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_pos_dict = user_pos_dict[0].tolist()
        print('用户自定义正面词', len(user_pos_dict))
        pos_dict.extend(user_pos_dict)
        print('合并后正面词', len(pos_dict))

    if user_neg and '.' in user_neg.filename and user_neg.filename.rsplit('.', 1)[1] == 'txt':
        fname = user_neg.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_neg_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_neg.save(os.path.join(file_dir, new_filename))
        user_neg_ans = True
        user_neg_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_neg_dict = user_neg_dict[0].tolist()
        print('用户自定义负面词词', len(user_neg_dict))
        neg_dict.extend(user_neg_dict)
        print('合并后负面词', len(neg_dict))

    ans = '自定义分词词典：' + str(user_fenci_ans) + ' ' + '自定义正面词词典：' + str(user_pos_ans) + ' ' + '自定义负面词词典：' + str(
        user_neg_ans)
    print(ans)
    return render_template("common_result.html",SuccessOrNot=1,ans=ans)


# get方式在地址栏会暴露内容，post不会
# 单弹幕分析
@app.route('/single_senti', methods=['GET', 'POST'])
def single_senti():
    single_text = request.form.get('single_text')
    if single_text is None:
        return render_template("single_senti.html", text="", ans=0)
    single_score = sentiment_single_result(single_text)
    if single_score > 0:
        ans = 1
    elif single_score == 0:
        ans = 0
    else:
        ans = -1
    return render_template("single_senti.html", text=single_text, ans=ans)


# 弹幕预处理页面
@app.route('/data_prepare')
def data_prepare():
    return render_template("data_prepare.html")


# 弹幕原始文件上传
@app.route('/danmu_upload', methods=['POST'], strict_slashes=False)
def danmu_upload():
    file_dir = 'E:/sentiment_system/danmu_data'  # 文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(file_dir, f.filename)
    if f and '.' in f.filename and f.filename.rsplit('.', 1)[1] == 'csv':  # 判断是否是允许上传的文件类型
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "danmu_original"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        f.save(os.path.join(file_dir, new_filename))
        SuccessOrNot = 1
        return render_template("upload_result.html", SuccessOrNot=SuccessOrNot)
    else:
        SuccessOrNot = 0
        return render_template("upload_result.html", SuccessOrNot=SuccessOrNot)


# 弹幕清洗
@app.route('/danmu_clean')
def danmu_clean():
    # 先判断弹幕原始数据是否已上传
    fin = r"E:/sentiment_system/danmu_data/danmu_original.csv"
    if not os.path.isfile(os.path.join(fin)):
        print("未上传弹幕原始数据")
        SuccessOrNot = 0
        ans = "未上传弹幕原始数据"
        return render_template("common_result.html",SuccessOrNot=SuccessOrNot,ans=ans)
    fout = r"E:/sentiment_system/danmu_data/danmu_cleaned.csv"
    run_data_clean(fin, fout)
    print("数据清洗完毕")
    SuccessOrNot=1
    ans="数据清洗完毕"
    return render_template("common_result.html",SuccessOrNot=SuccessOrNot,ans=ans)


# 已清洗文件下载
@app.route('/cleaned_download')
def cleaned_download():
    file_dir = 'E:/sentiment_system/danmu_data'  # 文件夹地址
    fname = "danmu_cleaned.csv"
    if os.path.isfile(os.path.join(file_dir, fname)):
        print(os.path.join(file_dir, fname))
        return send_from_directory(file_dir, fname, as_attachment=True)
    else:
        print('未找到已清洗文件')
        SuccessOrNot = 0
        ans = "未找到已清洗文件"
        return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)



# 按分钟聚合弹幕
@app.route('/danmu_frag')
def danmu_frag():
    # 先判断是否存在已清洗文件
    fin = r"E:/sentiment_system/danmu_data/danmu_cleaned.csv"
    if not os.path.isfile(os.path.join(fin)):
        print("未找到已清洗文件")
        SuccessOrNot = 0
        ans = "未找到已清洗文件"
        return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)

    fout = r"E:/sentiment_system/danmu_data/danmu_cleaned_frag.csv"
    danmu_60s_frag(fin, fout)
    print("数据聚合完毕")
    SuccessOrNot = 1
    ans = "数据聚合完毕"
    return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)


# 已聚合文件下载
@app.route('/cleaned_frag_download')
def cleaned_frag_donwload():
    file_dir = 'E:/sentiment_system/danmu_data'  # 文件夹地址
    fname = "danmu_cleaned_frag.csv"
    if os.path.isfile(os.path.join(file_dir, fname)):
        print(os.path.join(file_dir, fname))
        return send_from_directory(file_dir, fname, as_attachment=True)
    else:
        print('未找到已清洗后的弹幕片段文件')
        SuccessOrNot = 0
        ans = "未找到已清洗后的弹幕片段文件"
        return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)

# 提取情感特征
@app.route('/danmu_senti_feature')
def danmu_senti_feature():
    # 先判断是否存在已聚合文件
    fin = r"E:/sentiment_system/danmu_data/danmu_cleaned_frag.csv"
    if not os.path.isfile(os.path.join(fin)):
        print("未找到已清洗后的弹幕片段文件")
        SuccessOrNot = 0
        ans = "未找到已清洗后的弹幕片段文件"
        return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)
    fout = r"E:/sentiment_system/danmu_data/danmu_cleaned_frag_feature.csv"
    feature_danmu_frag(fin,fout)
    svm_model_test(fout,fout)
    print("提取情感特征完毕")
    SuccessOrNot = 1
    ans = "提取情感特征完毕"
    return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)

# 下载已提取情感特征的文件
@app.route('/cleaned_frag_feature_download')
def cleaned_frag_feature_download():
    file_dir = 'E:/sentiment_system/danmu_data'  # 文件夹地址
    fname = "danmu_cleaned_frag_feature.csv"
    if os.path.isfile(os.path.join(file_dir, fname)):
        print(os.path.join(file_dir, fname))
        return send_from_directory(file_dir, fname, as_attachment=True)
    else:
        print('未找到已提取情感特征的弹幕片段文件')
        SuccessOrNot = 0
        ans = "未找到已提取情感特征的弹幕片段文件"
        return render_template("common_result.html", SuccessOrNot=SuccessOrNot, ans=ans)

# 弹幕片段分析页面
@app.route('/frag_senti')
def frag_senti():
    return render_template("frag_senti.html")


# 上传处理后弹幕片段文件
@app.route('/frag_senti_upload', methods=['POST'], strict_slashes=False)
def frag_senti_upload():
    file_dir = 'E:/sentiment_system/frag_data'  # 文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(file_dir, f.filename)

    if f and '.' in f.filename and f.filename.rsplit('.', 1)[1] == 'csv':  # 判断是否是允许上传的文件类型
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "frag_file"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        f.save(os.path.join(file_dir, new_filename))
        SuccessOrNot = 1
        return render_template("upload_result.html", SuccessOrNot=SuccessOrNot)
    else:
        SuccessOrNot = 0
        return render_template("upload_result.html", SuccessOrNot=SuccessOrNot)


# 弹幕片段分析
@app.route('/frag_senti_analysis')
def frag_senti_analysis():
    # 先判断处理后弹幕片段数据是否已上传
    fin = r"E:/sentiment_system/frag_data/frag_file.csv"
    if not os.path.isfile(os.path.join(fin)):
        print("未上传弹幕片段文件")
        return "未上传弹幕片段文件"

    fout = r"E:/sentiment_system/frag_data/frag_report.txt"
    time, num, avg, pos_avg, neg_avg, pos_prop, neg_prop, senti_class = highlight.load_data(fin)
    # 生成分析报告
    highlight.senti_report(time, num, avg, pos_avg, neg_avg, pos_prop, neg_prop, senti_class, fout)
    senti_sum, pos_sum, neg_sum, neg_avg, pos_num, neg_num, senti_kinds, senti_prop = highlight.draw_senti(time, num,
                                                                                                           avg, pos_avg,
                                                                                                           neg_avg,
                                                                                                           pos_prop,
                                                                                                           neg_prop)

    # print(type(time),type(senti_kinds),type(senti_prop),type(pos_num),type(neg_num),type(avg))
    # print(type(pos_avg), type(neg_avg), type(senti_sum), type(pos_sum), type(neg_sum), type(num))
    # 12个变量
    return render_template("frag_senti_analysis.html", time=time, senti_kinds=senti_kinds, senti_prop=senti_prop,
                           num=num, pos_num=pos_num,
                           neg_num=neg_num, avg=avg, pos_avg=pos_avg, neg_avg=neg_avg, senti_sum=senti_sum,
                           pos_sum=pos_sum, neg_sum=neg_sum, )


# 分析报告下载
@app.route("/frag_senti_report")
def frag_senti_report():
    # 注意浏览器缓存问题
    file_dir = 'E:/sentiment_system/frag_data'  # 文件夹地址
    fname = "frag_report.txt"
    if os.path.isfile(os.path.join(file_dir, fname)):
        print(os.path.join(file_dir, fname))
        return send_from_directory(file_dir, fname, as_attachment=True)
    else:
        print('分析报告不存在')
        return "生成分析报告失败"


if __name__ == '__main__':
    app.run()
