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
			return render_template('succes.html')
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

@app.route('/search', methods=["GET","POST"])
def search():
	#if request.method == "GET":

	#	sel = db.execute("SELECT * from books where title='Krondor: The Betrayal'").fetchone()
	#	sel = str(sel).rstrip()
	#return sel

	if request.method == "POST":
		title_item = request.form.get("title")+'%'
		isbn_item = request.form.get("isbn")+'%'
		author_item = request.form.get("author")+'%'
		error_msg = "eroareeeee"
		title_req = db.execute("SELECT title, author from books where title like :search_r",
			{"search_r":title_item}).fetchone()
		isbn_req = db.execute("SELECT title, author from books where isbn like :isbn_r",
			{"isbn_r":isbn_item}).fetchone()
		author_req = db.execute("SELECT title, author from books where author like :author_r",
			{"author_r":author_item}).fetchone()
		#isbns = db.execute("SELECT isbn from books where isbn=:isb",
		#	{"isb":}).fetchall()
		
		if isbn_req is None:
			return render_template("search_result.html", search_res=error_msg)	
		else:
			return render_template("search_result.html", search_res=isbn_req)
		if title_req is None:
			return render_template("search_result.html", search_res=error_msg)
		else:
			return render_template("search_result.html", search_res=title_req) 
		if author_req is None:
			return render_template("search_result.html", search_res=error_msg)
		else:
			return render_template("search_result.html", search_res=author_req)

@app.route("/search/<int:book_id>")
def book(book_id):

	book_isbn = db.execute("SELECT isbn from books where isbn=:isbn_c",
		{"isbn_c":book_id}).fetchone()
	return render_template("search_result.html", search_res=book_isbn)
