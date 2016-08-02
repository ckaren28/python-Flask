from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
mysql = MySQLConnector(app,'emaildb')


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key = "oksowhatijustwanttogetthroughthisrightnowbecauseimsotiredandijustwanttogetitisall"

@app.route('/')
def index():
	query = "SELECT * FROM emails"                          
	email = mysql.query_db(query)    
	return render_template("index.html", emails = email)

@app.route('/process', methods=['POST'])
def result():
	if len(request.form['email']) < 1:
		flash("Email cannot be blank.")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
	else:	
		query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
		data = {
			'email': request.form['email']
		}
		mysql.query_db(query, data)
	return redirect('/') 

@app.route('/remove_friend/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)

# @app.route('/display', methods=['POST'])
# def display():
#      query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
#     data = {
#              'email': request.form['email']
#            }
#     mysql.query_db(query, data)
#     return redirect('/')


app.run(debug=True) # run our server

# time.strftime('%m-%d-%Y %H:%M')