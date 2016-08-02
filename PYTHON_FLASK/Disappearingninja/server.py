from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)
app.secret_key = "okokokoksoherewegoooooo"

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/ninja')
def ninja():
	source = "all.jpg"
	return render_template("ninja.html", source = source)

@app.route('/ninja/<color>')
def ninjachange(color):
	if color == "blue":
		source = "blue.jpg"
	elif color == "purple":
		source = "purple.jpg"
	elif color == "red":
		source = "red.jpg"
	elif color == "orange":
		source = "orange.jpg"
	else:
		source = "notapril.jpg"
	return render_template("ninja.html", source=source)


app.run(debug=True) # run our server