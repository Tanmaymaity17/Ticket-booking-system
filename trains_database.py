from mysql_connection import get_sql_connection
import sys
from subprocess import call

source = ''
destination = ''
date = ''


def open_trains_list(date, response):
    response_str = " , ".join(map(str, response))
    call(["python", "trains_list.py", date, response_str])


def fetch_details():
    global source, destination, date
    if len(sys.argv) == 4:
        source, destination, date = sys.argv[1:]

    else:
        source = 'Mumbai'
        destination = 'Kolkata'
        date = '2024-03-19'


def get_all_trains(connection):
    global source, destination, date
    fetch_details()

    cursor = connection.cursor()

    query = "SELECT t.*, st.ac_seats, st.sleep_seats " \
            "FROM booking_system.trains t " \
            "JOIN booking_system.seats_trains st ON t.trainID = st.trainID " \
            "WHERE t.source = %s AND t.destination = %s AND st.date = %s"

    cursor.execute(query, (source, destination, date))

    response = []

    for (trainID, name, source, destination, ac_fare, sleep_fare, ac_seats, sleep_seats) in cursor:
        response.append(
           {
               'trainID': trainID,
               'name': name,
               'source': source,
               'destination': destination,
               'ac_fare': ac_fare,
               'sleep_fare': sleep_fare,
               'ac_seats': ac_seats,
               'sleep_seats': sleep_seats
           }
        )

    return response


if __name__ == '__main__':
    print("Arguments:", sys.argv)  # Debug print
    connection = get_sql_connection()
    response = get_all_trains(connection)
    print(response)
    open_trains_list(date, response)
