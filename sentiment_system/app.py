from flask import Flask,render_template,request
from sentiment_by_dict import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

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


if __name__ == '__main__':
    app.run()
