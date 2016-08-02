from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
	print "here"
	# recall the name attributes we added to our form inputs
	# to access the data that the user input into the fields we use request.form['name_of_input']
	name = request.form['name']
	location = request.form['loc']
	lang = request.form['lang']
	comment = request.form['comment']
	return render_template('result.html', name=name, location = location, lang = lang, comment= comment) # redirects back to the '/' route
	# return redirect('/')

app.run(debug=True) # run our server