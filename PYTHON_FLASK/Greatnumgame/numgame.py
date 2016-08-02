from flask import Flask, render_template, request, redirect, session
import random 
app = Flask(__name__)
app.secret_key = "blahblahblah"

@app.route('/')
def index():
    if not 'answer' in session.keys():
        session['answer'] = random.randrange(0, 101)
# session.pop('answer')
    print session.keys()
    yes = "hidden"
    high = "hidden"
    low = "hidden"
    num = session["answer"]
    if not 'num' in session.keys():
        return render_template("index.html", yes = yes, high = high, low = low, num= num)
    if session["num"] == session['answer']:
        yes = " "
    elif session['num'] > session['answer']:
        high = " "
    elif session['num'] < session['answer']:
        low = " "
    else:
        yes =" "
    return render_template("index.html", yes = yes, high = high, low = low, num= num)


@app.route('/guess', methods=['POST'])
def choose_num():
    print "Getting guess"
    session['num'] = int(request.form['num'])
    print "num"

    return redirect('/')


@app.route('/result', methods=['POST'])
def show_user():
    session.pop('answer')
    session.pop('num')
    return redirect('/')



app.run(debug=True) 