from flask import Flask, render_template, request, redirect,session, flash

app = Flask(__name__)
app.secret_key = "iwanttosmokehellaweedsrightnow"

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
	name = request.form['name']
	location = request.form['loc']
	lang = request.form['lang']
	comment = request.form['comment']
	if len(request.form['name']) < 1:
		flash("Name can't be empty bitch.")
		return redirect('/')
	print len(request.form['comment'])
	if len(request.form['comment']) < 2:
		flash("Comments can't be blank like your personality.")
		return redirect('/')
	elif len(request.form['comment'])>120:
		flash("That's too long bitch.")
		return redirect('/')
	return render_template('result.html', name=name, location = location, lang = lang, comment= comment) 

app.run(debug=True) # run our server