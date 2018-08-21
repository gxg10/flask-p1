import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	f = open('books.csv')
	reader = csv.reader(f)	
	next(reader,None)
	for nr, titlu, autor, an in reader:
		db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
			{"isbn":nr, "title":titlu,"author":autor, "year":an})

	db.commit()
if __name__=="__main__":
	main()