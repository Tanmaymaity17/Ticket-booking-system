from mysql_connection import get_sql_connection
import sys
from subprocess import call

source = ''
destination = ''
date = ''


def open_flights_list(date, response):
    response_str = " , ".join(map(str, response))
    call(["python", "flights_list.py", date, response_str])


def fetch_details():
    global source, destination, date
    if len(sys.argv) == 4:
        source, destination, date = sys.argv[1:]

    else:
        source = 'Mumbai'
        destination = 'Kolkata'
        date = '2024-03-19'


def get_all_flights(connection):
    global source, destination, date
    fetch_details()

    cursor = connection.cursor()

    query = "SELECT f.*, sf.eco_seats, sf.busn_seats " \
            "FROM booking_system.flights f " \
            "JOIN booking_system.seats_flights sf ON f.flightID = sf.flightID " \
            "WHERE f.source = %s AND f.destination = %s AND sf.date = %s"

    cursor.execute(query, (source, destination, date))

    response = []

    for (flightID, name, source, destination, eco_fare, busn_fare, eco_seats, busn_seats) in cursor:
        response.append(
           {
               'flightID': flightID,
               'name': name,
               'source': source,
               'destination': destination,
               'eco_fare': eco_fare,
               'busn_fare': busn_fare,
               'eco_seats': eco_seats,
               'busn_seats': busn_seats
           }
        )

    return response


if __name__ == '__main__':
    print("Arguments:", sys.argv)  # Debug print
    connection = get_sql_connection()
    response = get_all_flights(connection)
    print(response)
    open_flights_list(date, response)
