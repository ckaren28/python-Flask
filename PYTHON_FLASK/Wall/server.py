from flask import Flask, render_template, request, redirect,session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
PW_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]*$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "whackattacktoturnyouback"
mysql = MySQLConnector(app,'walldb')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
	query_data = {'email': email}
	user = mysql.query_db(user_query, query_data)
	print user
	if bcrypt.check_password_hash(user[0]['pw_hash'], password):
		# if not 'user' in session.keys():
		# 	session['user'] = user[0]['first_name']
		# 	session['id'] = user[0]['id']
		# 	print "whatwhat"
		# else:
			session['user'] = user[0]['first_name']
			session['id'] = user[0]['id']
			print session['id']
			print session
			print 'hello'
			return redirect('/wall')
		#login user
	else:
		flash("Not a Valid Username")
		return render_template("index.html", user = user)

@app.route('/registerpage', methods=['POST','GET'])
def register():
	return render_template("reg.html")

@app.route('/back', methods=['POST'])
def back():
	return redirect("/")

@app.route('/create_user', methods=['POST'])
def create_user():
	has_errors = False;
	if request.form:
		if len(request.form['first_name']) <= 2:
			flash("First Name cannot be blank.")
			has_errors = True;
		elif not NAME_REGEX.match(request.form['first_name']):
			flash("first name can't have a number in it.")
			has_errors = True;
		if len(request.form['last_name']) <= 2:
			flash("Lastname cannot be blank.")
			has_errors = True;
		elif not NAME_REGEX.match(request.form['last_name']):
			flash("last name can't have a number in it.")
			has_errors = True;
		if len(request.form['email']) < 1:
			flash("Email cannot be blank.")
			has_errors = True;
		elif not EMAIL_REGEX.match(request.form['email']):
			flash("Invalid Email Address!")
			has_errors = True;
		if len(request.form['password']) < 8:
			flash("Password has to be longer than eight chars.")
			has_errors = True;
		elif request.form['password']!= request.form['confirmpw'] :
			flash("Password has to match.")
			has_errors = True;
		if has_errors == False:
			flash("submitted!")
			email = request.form['email']
			password = request.form['password']
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			pw_hash = bcrypt.generate_password_hash(password)
			insert_query = "INSERT INTO users (email, first_name, last_name, pw_hash, created_at, updated_at) VALUES (:email, :first_name, :last_name, :pw_hash, NOW(), NOW())"
			query_data = { 'email': email, 'first_name': first_name, 'last_name': last_name, 'pw_hash': pw_hash}
			mysql.query_db(insert_query, query_data)
			return redirect('/')

@app.route('/wall', methods=['POST', 'GET'])
def wall():
	user = session['user']
	join_querry = "SELECT messages.message, messages.created_at, messages.id, users.first_name, users.last_name FROM messages JOIN users ON users.id = messages.users_id "
	messages = mysql.query_db(join_querry)
	print messages

	joint_query = "SELECT comment.comment, comment.created_at, comment.messages_id, users.first_name, users.last_name FROM comment JOIN users ON users.id = comment.users_id"
	comments = mysql.query_db(joint_query)
	print comments

	return render_template('comments.html', user = user, messages = messages, comments = comments)


@app.route('/postc/<message_id>', methods=['POST'])
def postcomment(message_id):
	query = "INSERT INTO comment (users_id, comment, messages_id, created_at, updated) VALUES (:users_id, :comment, :messages_id, NOW(), NOW())"
	data = {
		'comment':request.form['comment'],
		'users_id': session['id'],
		'messages_id': message_id 
	}
	mysql.query_db(query, data)

	return redirect('/wall')

@app.route('/postm', methods=['POST'])
def postmessage():
	query = "INSERT INTO messages (users_id, message, created_at, updated_at) VALUES (:users_id, :message, NOW(), NOW())"
	data = {
             'message': request.form['message'],
             'users_id' : session['id']
           }

	mysql.query_db(query, data)
	return redirect("/wall")

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	print"hey"
	return redirect('/')



app.run(debug=True)