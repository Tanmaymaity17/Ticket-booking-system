import tkinter as tk
from flights_database import get_all_flights
from mysql_connection import get_sql_connection
from subprocess import call
import sys


def open_book_flight_file(flight):
    call(["python", "bookFlightTicketForm.py", str(flight['flightID']), str(flight['name']), str(flight['source']),
          str(flight['destination']),
          str(flight['eco_fare']),
          str(flight['busn_fare']),
          str(date)])


def display_flights(all_flights):

    flights_window = tk.Tk()
    flights_window.title("List of Flights")
    flights_window.configure(bg='#acfcfc')

    # Create labels for headers
    label_train_id = tk.Label(flights_window, text="Flight ID", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_train_id.grid(row=0, column=0)
    label_train_name = tk.Label(flights_window, text="Flight Name", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_train_name.grid(row=0, column=1)
    label_source = tk.Label(flights_window, text="Source", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_source.grid(row=0, column=2)
    label_destination = tk.Label(flights_window, text="Destination", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_destination.grid(row=0, column=3)
    label_eco_fare = tk.Label(flights_window, text="Economy Fare", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_eco_fare.grid(row=0, column=4)
    label_busn_fare = tk.Label(flights_window, text="Business Fare", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_busn_fare.grid(row=0, column=5)
    label_eco_seats = tk.Label(flights_window, text="Economy Seats", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_eco_seats.grid(row=0, column=6)
    label_busn_seats = tk.Label(flights_window, text="Business Seats", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_busn_seats.grid(row=0, column=7)
    label_book = tk.Label(flights_window, text="Book", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_book.grid(row=0, column=8)

    row_counter = 1  # Keep track of row for data placement

    # Display train data using labels
    for flight in all_flights:
        label_id = tk.Label(flights_window, text=flight['flightID'], bg='#acfcfc', fg='#000000')
        label_id.grid(row=row_counter, column=0)
        label_name = tk.Label(flights_window, text=flight['name'], bg='#acfcfc', fg='#000000')
        label_name.grid(row=row_counter, column=1)
        label_source_city = tk.Label(flights_window, text=flight['source'], bg='#acfcfc', fg='#000000')
        label_source_city.grid(row=row_counter, column=2)
        label_destination_city = tk.Label(flights_window, text=flight['destination'], bg='#acfcfc', fg='#000000')
        label_destination_city.grid(row=row_counter, column=3)
        label_eco_fare = tk.Label(flights_window, text=flight['eco_fare'], bg='#acfcfc', fg='#000000')
        label_eco_fare.grid(row=row_counter, column=4)
        label_busn_fare = tk.Label(flights_window, text=flight['busn_fare'], bg='#acfcfc', fg='#000000')
        label_busn_fare.grid(row=row_counter, column=5)
        label_eco_seats = tk.Label(flights_window, text=flight['eco_seats'], bg='#acfcfc', fg='#000000')
        label_eco_seats.grid(row=row_counter, column=6)
        label_busn_seats = tk.Label(flights_window, text=flight['busn_seats'], bg='#acfcfc', fg='#000000')
        label_busn_seats.grid(row=row_counter, column=7)
        # Create a book button for each train
        book_button = tk.Button(flights_window, text="Book", bg='#fcc44c', fg='#000000',
                                command=lambda f=flight: open_book_flight_file(f))
        book_button.grid(row=row_counter, column=8)
        row_counter += 1  # Move to next row for the next train

    flights_window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        date = sys.argv[1]
        all_flights_str = sys.argv[2]
        all_flights = eval(all_flights_str)
        print(all_flights)
        display_flights(all_flights)
    else:
        connection = get_sql_connection()
        all_flights = get_all_flights(connection)
        connection.close()
        display_flights(all_flights)
