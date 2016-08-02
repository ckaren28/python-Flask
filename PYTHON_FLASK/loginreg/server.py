from flask import Flask, render_template, request, redirect,session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
PW_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]*$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "okivebeenfeelingprettygoodtodayitsnottoohotandnottoocoldoutside"
mysql = MySQLConnector(app,'registration')


@app.route('/', methods=['GET'])
def index():
  return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	user_query = "SELECT * FROM registration WHERE email = :email LIMIT 1"
	query_data = {'email': email}
	user = mysql.query_db(user_query, query_data)
	print user
	if bcrypt.check_password_hash(user[0]['pw_hash'], password):
		return render_template('success.html')
		#login user
	else:
		flash("Not a Valid Username")
		return render_template("login.html", user = user)

@app.route('/registerpage', methods=['POST','GET'])
def register():
	return render_template("reg.html")

@app.route('/back', methods=['POST'])
def back():
	return redirect("/")

@app.route('/create_user', methods=['POST'])
def create_user():
	if request.form:
		print "ajdflkajsdlk;f"
		if len(request.form['first_name']) <= 2:
			flash("First Name cannot be blank.")
			return redirect('/registerpage')
		elif not NAME_REGEX.match(request.form['first_name']):
			flash("first name can't have a number in it.")
			return redirect('/registerpage')
		if len(request.form['last_name']) <= 2:
			flash("Lastname cannot be blank.")
			return redirect('/registerpage')
		elif not NAME_REGEX.match(request.form['last_name']):
			flash("last name can't have a number in it.")
			return redirect('/registerpage')
		if len(request.form['email']) < 1:
			flash("Email cannot be blank.")
			return redirect('/registerpage')
		elif not EMAIL_REGEX.match(request.form['email']):
			flash("Invalid Email Address!")
			return redirect('/registerpage')
		if len(request.form['password']) < 8:
			flash("Password has to be longer than eight chars.")
			return redirect('/registerpage')
		elif request.form['password']!= request.form['confirmpw'] :
			flash("Password has to match.")
			return redirect('/registerpage')
		else:
			flash("submitted!")
			email = request.form['email']
			password = request.form['password']
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			pw_hash = bcrypt.generate_password_hash(password)
			insert_query = "INSERT INTO registration (email, first_name, last_name, pw_hash, created_at) VALUES (:email, :first_name, :last_name, :pw_hash, NOW())"
			query_data = { 'email': email, 'first_name': first_name, 'last_name': last_name, 'pw_hash': pw_hash}
			mysql.query_db(insert_query, query_data)
			return render_template('success.html')







app.run(debug=True)