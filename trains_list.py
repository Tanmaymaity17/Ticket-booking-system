import tkinter as tk
from trains_database import get_all_trains
from mysql_connection import get_sql_connection
from subprocess import call
import sys


def open_book_train_file(train):
    call(["python", "bookTrainTicketForm.py", str(train['trainID']), str(train['name']), str(train['source']),
          str(train['destination']),
          str(train['ac_fare']),
          str(train['sleep_fare']),
          str(date)])


def display_trains(all_trains):

    trains_window = tk.Tk()
    trains_window.title("List of Trains")
    trains_window.configure(bg='#acfcfc')

    # Create labels for headers
    label_train_id = tk.Label(trains_window, text="Train ID", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_train_id.grid(row=0, column=0)
    label_train_name = tk.Label(trains_window, text="Train Name", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_train_name.grid(row=0, column=1)
    label_source = tk.Label(trains_window, text="Source", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_source.grid(row=0, column=2)
    label_destination = tk.Label(trains_window, text="Destination", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_destination.grid(row=0, column=3)
    label_ac_fare = tk.Label(trains_window, text="Ac Fare", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_ac_fare.grid(row=0, column=4)
    label_sleep_fare = tk.Label(trains_window, text="Sleeper Fare", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_sleep_fare.grid(row=0, column=5)
    label_ac_seats = tk.Label(trains_window, text="Ac Seats", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_ac_seats.grid(row=0, column=6)
    label_sleep_seats = tk.Label(trains_window, text="Sleeper Seats", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_sleep_seats.grid(row=0, column=7)
    label_book = tk.Label(trains_window, text="Book", bg='#131166', fg='#ffffff', font=('Arial', 12))
    label_book.grid(row=0, column=8)

    row_counter = 1  # Keep track of row for data placement

    # Display train data using labels
    for train in all_trains:
        label_id = tk.Label(trains_window, text=train['trainID'], bg='#acfcfc', fg='#000000')
        label_id.grid(row=row_counter, column=0)
        label_name = tk.Label(trains_window, text=train['name'], bg='#acfcfc', fg='#000000')
        label_name.grid(row=row_counter, column=1)
        label_source_city = tk.Label(trains_window, text=train['source'], bg='#acfcfc', fg='#000000')
        label_source_city.grid(row=row_counter, column=2)
        label_destination_city = tk.Label(trains_window, text=train['destination'], bg='#acfcfc', fg='#000000')
        label_destination_city.grid(row=row_counter, column=3)
        label_ac_fare = tk.Label(trains_window, text=train['ac_fare'], bg='#acfcfc', fg='#000000')
        label_ac_fare.grid(row=row_counter, column=4)
        label_sleep_fare = tk.Label(trains_window, text=train['sleep_fare'], bg='#acfcfc', fg='#000000')
        label_sleep_fare.grid(row=row_counter, column=5)
        label_ac_seats = tk.Label(trains_window, text=train['ac_seats'], bg='#acfcfc', fg='#000000')
        label_ac_seats.grid(row=row_counter, column=6)
        label_sleep_seats = tk.Label(trains_window, text=train['sleep_seats'], bg='#acfcfc', fg='#000000')
        label_sleep_seats.grid(row=row_counter, column=7)
        # Create a book button for each train
        book_button = tk.Button(trains_window, text="Book", bg='#fcc44c', fg='#000000',
                                command=lambda t=train: open_book_train_file(t))
        book_button.grid(row=row_counter, column=8)
        row_counter += 1  # Move to next row for the next train

    trains_window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        date = sys.argv[1]
        all_trains_str = sys.argv[2]
        all_trains = eval(all_trains_str)
        print(date)
        print(all_trains)
        display_trains(all_trains)
    else:
        connection = get_sql_connection()
        all_trains = get_all_trains(connection)
        connection.close()
        display_trains(all_trains)
