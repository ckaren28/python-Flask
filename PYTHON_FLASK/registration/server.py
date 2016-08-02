from flask import Flask, render_template, request, redirect,session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
PW_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]*$')
app = Flask(__name__)
app.secret_key = "iwanttosmokehellaweedsrightnow"

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

@app.route('/proccess', methods=['POST'])
def submit():
	print EMAIL_REGEX.match(request.form['email'])
	if len(request.form['fname']) < 1:
		flash("First Name cannot be blank.")
	elif not NAME_REGEX.match(request.form['fname']):
		flash("first name can't have a number in it.")
	if len(request.form['lname']) < 1:
		flash("Lastname cannot be blank.")
	elif not NAME_REGEX.match(request.form['lname']):
		flash("last name can't have a number in it.")
	if len(request.form['email']) < 1:
		flash("Email cannot be blank.")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
	if len(request.form['pw']) < 8:
		flash("Password has to be longer than eight chars.")
	elif request.form['pw']!= request.form['confirmpw'] :
		flash("Password has to match.")
	elif not PW_REGEX.match(request.form['pw']):
		flash("Password needs lower and uppercase characters.")
	else:
		flash("YES.")
	return redirect('/') 

app.run(debug=True) # run our server