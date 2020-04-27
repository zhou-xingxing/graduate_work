from flask import Flask,render_template,request,send_from_directory
from sentiment_by_dict import *
import highlight

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dict_page')
def dict_page():
    return render_template("dict_page.html")

# 上传自定义词典并合并
@app.route('/user_dict_upload', methods=['POST'], strict_slashes=False)
def user_dict_upload():
    file_dir = 'E:/sentiment_system/user_dict' # 文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    user_fenci = request.files['fenci_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    user_pos = request.files['pos_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    user_neg = request.files['neg_dict']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(file_dir,user_fenci.filename,user_pos.filename,user_neg.filename)
    user_fenci_ans,user_pos_ans,user_neg_ans=False,False,False
    if user_fenci and '.' in user_fenci.filename and user_fenci.filename.rsplit('.', 1)[1]=='txt':
        fname=user_fenci.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_fenci_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_fenci.save(os.path.join(file_dir, new_filename))
        user_fenci_ans=True
        user_fenci_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_fenci_dict = user_fenci_dict[0].tolist()
        print('用户自定义分词个数',len(user_fenci_dict))
        for i in user_fenci_dict:
            jieba.add_word(i)

    if user_pos and '.' in user_pos.filename and user_pos.filename.rsplit('.', 1)[1]=='txt':
        fname=user_pos.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_pos_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_pos.save(os.path.join(file_dir, new_filename))
        user_pos_ans=True
        user_pos_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_pos_dict = user_pos_dict[0].tolist()
        print('用户自定义正面词',len(user_pos_dict))
        pos_dict.extend(user_pos_dict)
        print('合并后正面词',len(pos_dict))

    if user_neg and '.' in user_neg.filename and user_neg.filename.rsplit('.', 1)[1]=='txt':
        fname=user_neg.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name = "user_neg_dict"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        user_neg.save(os.path.join(file_dir, new_filename))
        user_neg_ans=True
        user_neg_dict = pd.read_csv(os.path.join(file_dir, new_filename), header=None)
        user_neg_dict = user_neg_dict[0].tolist()
        print('用户自定义负面词词', len(user_neg_dict))
        neg_dict.extend(user_neg_dict)
        print('合并后负面词', len(neg_dict))

    ans='自定义分词词典：'+str(user_fenci_ans)+'\n'+'自定义正面词词典：'+str(user_pos_ans)+'\n'+'自定义负面词词典：'+str(user_neg_ans)
    print(ans)
    return ans



# get方式在地址栏会暴露内容，post不会
@app.route('/single_senti', methods=['GET', 'POST'])
def single_senti():
    single_text=request.form.get('single_text')
    if single_text is None:
        return render_template("single_senti.html", text="",ans=0)
    single_score=sentiment_single_result(single_text)
    if single_score>0:
        ans=1
    elif single_score==0:
        ans=0
    else:
        ans=-1
    return render_template("single_senti.html",text=single_text,ans=ans)

@app.route('/frag_senti')
def frag_senti():
    return render_template("frag_senti.html")

# 上传弹幕片段文件
@app.route('/frag_senti_upload', methods=['POST'], strict_slashes=False)
def frag_senti_upload():
    file_dir = 'E:/sentiment_system/frag_data' # 文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print(file_dir,f.filename)

    if f and '.' in f.filename and f.filename.rsplit('.', 1)[1]=='csv':  # 判断是否是允许上传的文件类型
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        new_name="frag_file"
        new_filename = new_name + '.' + ext  # 修改文件名
        # 只接受绝对路径
        f.save(os.path.join(file_dir, new_filename))
        SuccessOrNot=1
        return render_template("frag_senti_upload.html",SuccessOrNot=SuccessOrNot)
    else:
        SuccessOrNot=0
        return render_template("frag_senti_upload.html",SuccessOrNot=SuccessOrNot)

@app.route('/frag_senti_analysis')
def frag_senti_analysis():
    # 先判断弹幕片段数据是否已上传
    fin = r"E:/sentiment_system/frag_data/frag_file.csv"
    if os.path.isfile(os.path.join(fin))==False:
        print("未上传弹幕片段文件")
        return "未上传弹幕片段文件"

    fout =r"E:/sentiment_system/frag_data/frag_report.txt"
    time, num, avg, pos_avg, neg_avg, pos_prop, neg_prop, senti_class = highlight.load_data(fin)
    highlight.senti_report(time, num, avg, pos_avg, neg_avg, pos_prop, neg_prop, senti_class,fout)

    return render_template("frag_senti_analysis.html")

@app.route("/frag_senti_report")
def frag_senti_report():
    # 注意浏览器缓存问题
    file_dir = 'E:/sentiment_system/frag_data'  # 文件夹地址
    fname="frag_report.txt"
    if os.path.isfile(os.path.join(file_dir, fname)):
        print(os.path.join(file_dir, fname))
        return send_from_directory(file_dir, fname, as_attachment=True)
    else:
        print('文件不存在')
        return "还未生成分析报告"

if __name__ == '__main__':
    app.run()
