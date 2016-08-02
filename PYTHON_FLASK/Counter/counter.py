from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "ThisIsSecret"

@app.route('/')
def index():
	if not 'count'in session.keys():
		session['count'] = 1
	else:
		session['count'] += 1
	# if session['count'] == None:
	# 	pass
	return render_template("index.html")



# @app.route('/', methods=['POST'])
# def counting():
# 	if 'user' in session == "K":
# 		count = count + 1
# 	# return render_template("index.html", count = count)
# 	return redirect('/', count  + 1)



# @app.route('/show')
# def show_user():
#   return render_template('index.html')





app.run(debug=True) # run our server