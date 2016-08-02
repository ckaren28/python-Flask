from flask import Flask, render_template, request, redirect, session
import random, datetime
app = Flask(__name__)
app.secret_key = "blahblahblah"


@app.route('/')
def index():
	if not 'score' in session.keys():
		session['score'] = 0
	if not 'log' in session.keys():
		session['log'] = "  "
	return render_template("index.html", score = session['score'], log = session['log'])
		# , log = session["log"])


@app.route('/process_money', methods=['POST'])
def choose_num():
	date = datetime.datetime.now()
	gold = 'gold'
	log = 'log'
	if request.form['building'] == 'farm':
		gold = random.randrange(10,20)
		session['score'] += gold
		session['log'] += "<p> Earned " + str(gold) + " gold from the farm! ( " + date.strftime("%Y/%m/%d %I:%M") + " ) </p>" 
		print log
	elif request.form['building'] == 'cave':
		gold = random.randrange(5,10)
		session['score'] += gold
		session['log'] += "<p> Earned " + str(gold) + " gold from the cave! ( " + date.strftime("%Y/%m/%d %I:%M") + " )</p>"
		print log
	elif request.form['building'] == 'house':
		gold = random.randrange(2,5)
		session['score'] += gold
		session['log'] += "<p> Earned " + str(gold) + " gold from the house! ( " + date.strftime("%Y/%m/%d %I:%M") + " )</p>"
		print log
	elif request.form['building'] == 'casino':
		gold = random.randrange(-50,50)
		session['score'] += gold
		if gold < 0:
			session['log'] += "<p style= 'color:red;'>Entered a casino and lost " + str(gold * -1) + " golds...OUCH...( " + date.strftime("%Y/%m/%d %I:%M") + " ) </p>"
		else:
			session['log'] += "<p> Earned " + str(gold) + " gold from the casino! ( " + date.strftime("%Y/%m/%d %I:%M") + " ) </p>"
		print log
	return redirect('/')

@app.route('/reset', methods=['POST'])
def reset_game():
    session.pop('log')
    session.pop('score')
    return redirect('/')


app.run(debug=True) 