import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	if not session['logged_in']:
		return login()
	else:
		return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
	if request.method == "POST":
		user = request.form.get("user")
		password = request.form.get("password")
		if password== "123" and user=="admin":
			session['logged_in'] = True
			return "contrats"
		else:
			flash('wrong password')
			return index()
	return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return render_template('logout.html')

@app.route('/books', methods=["GET","POST"])
def books():
	if request.method == "GET":

		sel = db.execute("SELECT * from books where title='Krondor: The Betrayal'").fetchone()
	
	return sel


