import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

	flights = db.execute("SELECT id, origin, destination, duration FROM flights").fetchall()

	for flight in flights:
		print (f"flight {flight.id}:{flight.origin} to {flight.destination} minutes")

	flight_id = int(input("\nFlight ID: "))

	flight = db.execute("SELECT origin, destination, duration FROM flights WHERE id = :id",
		{"id":flight_id}).fetchone()

	if flight is None:
		print("error: no such flight.")
		return

	passengers = db.execute("SELECT name from passengers where flight_id = :flight_id",
		{"flight_id":flight_id}).fetchall()

	print ("\nPassengers:")
	for passenger in passengers:
		print(passenger.name)
	if len(passengers) == 0:
		print("No passengers")

if __name__ == "__main__":
	main()