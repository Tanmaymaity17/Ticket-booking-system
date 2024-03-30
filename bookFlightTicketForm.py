import tkinter
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
from tkinter import messagebox
from docx2pdf import convert
import sys
from mysql_connection import get_sql_connection_1

# Define global variables
source = None
destination = None
date = None
flightID = None
flightName = None
fare = 0
last_booking_id = 101

# Global variable to store the number of passengers
passenger_count = 0


def get_booking_id():
    global last_booking_id
    new_booking_id = last_booking_id + 1
    last_booking_id = new_booking_id

    return str(new_booking_id)


def fetch_details():
    global source, destination, date, flightID, flightName, fare
    if len(sys.argv) == 8:  # Ensure correct number of arguments are provided
        # Extract command-line arguments
        flightID, flightName, source, destination, eco_fare, busn_fare, date = sys.argv[1:]
        # Assign fetched values to global variables
        source = source
        destination = destination
        date = date
        flightName = flightName
        if class_entry.get() == "Economy":
            fare = int(eco_fare) if eco_fare.isdigit() else 1000
        elif class_entry.get() == "Business":
            fare = int(busn_fare) if busn_fare.isdigit() else 500
    else:
        # For testing purposes, defining variables manually
        source = "TestSource"
        destination = "TestDestination"
        date = "20-03-2024"
        flightID = '12345'
        flightName = "TestFlight"
        if class_entry.get() == "Economy":
            fare = 1000
        elif class_entry.get() == "Business":
            fare = 500


def clear_item():
    passName_entry.delete(0, tkinter.END)
    age_entry.delete(0, tkinter.END)
    age_entry.insert(0, "1")
    gender_entry.set("")


ticket_list = []


def add_item():
    global passenger_count
    Pname = passName_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    Pclass = class_entry.get()
    ticket_item = [Pname, age, gender, Pclass]

    tree.insert('', 0, values=ticket_item)
    clear_item()
    ticket_list.append(ticket_item)
    passenger_count += 1  # Increment passenger count when an item is added


def new_ticket():
    global passenger_count
    name_entry.delete(0, tkinter.END)
    flightID_entry.delete(0, tkinter.END)
    class_entry.set("")
    clear_item()
    tree.delete(*tree.get_children())
    ticket_list.clear()
    passenger_count = 0


def generate_ticket():
    connection = get_sql_connection_1()
    print(connection)
    fetch_details()
    cursor = connection.cursor()
    fetch_details()

    doc = DocxTemplate("plane_ticket_template.docx")
    name = name_entry.get()

    # Initialize seat number
    seat_number = 20
    print(len(ticket_list))
    seat_count = len(ticket_list)
    print(cursor)
    print(seat_count)
    # For AC class
    if class_entry.get() == 'Economy':
        query = ("UPDATE booking_system.seats_flights SET eco_seats = eco_seats - %s WHERE flightID = %s "
                 "AND date = %s;")
        try:
            cursor.execute(query, (seat_count, flightID, date))
            connection.commit()
            print("Economy seats updated successfully.")
        except Exception as e:
            print("Error updating Economy seats:", e)

    # For Sleeper class
    elif class_entry.get() == 'Business':
        query = ("UPDATE booking_system.seats_flights SET busn_seats = busn_seats - %s WHERE flightID = %s "
                 "AND date = %s;")
        try:
            cursor.execute(query, (seat_count, flightID, date))
            connection.commit()
            print("Business seats updated successfully.")
        except Exception as e:
            print("Error updating Business seats:", e)

    # Iterate over each ticket item and assign seat number
    for ticket_item in ticket_list:
        ticket_item.append(seat_number)
        seat_number += 1

    subtotal = fare * passenger_count
    platformFee = (fare * 0.01) * passenger_count
    total = subtotal + platformFee

    doc.render({"fname": name,
                "flightID": flightID,
                "source": source,
                "destination": destination,
                "date": date,
                "bookingID": get_booking_id(),
                "flightName": flightName,
                "ticket_list": ticket_list,
                "subtotal": subtotal,
                "platformFee": platformFee,
                "total": total
                })

    doc_name = "flight-ticket_" + name + datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S") + ".docx"
    doc.save(doc_name)

    # Convert generated docx ticket to pdf and save into the "Tickets" folder
    generate_pdf(doc_name)

    messagebox.showinfo("Ticket Booked", "Ticket Booked Successfully")

    new_ticket()


def generate_pdf(docx_file_path):
    try:
        # Convert docx to pdf and specify the output folder
        convert(docx_file_path)
        print("PDF generated successfully.")
    except Exception as e:
        print("Error generating PDF:", e)


bookingPage = tkinter.Tk()
bookingPage.title("Ticket Booking Form")
bookingPage.configure(bg='#1d91cc')

frame = tkinter.Frame(bookingPage)
frame.pack(padx=20, pady=10)
frame.configure(bg='#1d91cc')

name_label = tkinter.Label(frame, text="Name", bg='#105274', fg='#FFFFFF', font='Arial')
name_label.grid(row=0, column=0)
flightID_label = tkinter.Label(frame, text="Flight No.", bg='#105274', fg='#FFFFFF', font='Arial')
flightID_label.grid(row=0, column=1)
class_label = tkinter.Label(frame, text="Class", bg='#105274', fg='#FFFFFF', font='Arial')
class_label.grid(row=0, column=2)

name_entry = tkinter.Entry(frame)
name_entry.grid(row=1, column=0)
flightID_entry = tkinter.Entry(frame)
flightID_entry.grid(row=1, column=1)

class_entry = tkinter.StringVar()
class_drop_down = ttk.Combobox(frame, textvariable=class_entry)
class_drop_down['values'] = ('Economy', 'Business')
class_drop_down.grid(row=1, column=2)

passName_label = tkinter.Label(frame, text="Passenger Name", bg='#105274', fg='#FFFFFF', font='Arial')
passName_label.grid(row=2, column=0)
age_label = tkinter.Label(frame, text="Age", bg='#105274', fg='#FFFFFF', font='Arial')
age_label.grid(row=2, column=1)
gender_label = tkinter.Label(frame, text="Gender", bg='#105274', fg='#FFFFFF', font='Arial')
gender_label.grid(row=2, column=2)

passName_entry = tkinter.Entry(frame)
passName_entry.grid(row=3, column=0)
age_entry = tkinter.Spinbox(frame, from_=1, to=100, increment=1)
age_entry.grid(row=3, column=1)

gender_entry = tkinter.StringVar()
gender_drop_down = ttk.Combobox(frame, textvariable=gender_entry)
gender_drop_down['values'] = ('Male', 'Female')
gender_drop_down.grid(row=3, column=2)

add_item_button = tkinter.Button(frame, text="Add passenger", bg='#d4e9f0', fg='#1c120c', command=add_item)
add_item_button.grid(row=4, column=2, pady=5)

columns = ('Name', 'Age', 'Gender', 'Class')
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('Name', text='Name')
tree.heading('Age', text='Age')
tree.heading('Gender', text='Gender')
tree.heading('Class', text='Class')

tree.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

save_ticket_button = tkinter.Button(frame, text="Confirm Booking", bg='#d4e9f0', fg='#1c120c', command=generate_ticket)
save_ticket_button.grid(row=6, column=0, columnspan=3, sticky="news", padx=20, pady=5)
new_ticket_button = tkinter.Button(frame, text="Clear All", bg='#d4e9f0', fg='#1c120c', command=new_ticket)
new_ticket_button.grid(row=7, column=0, columnspan=3, sticky="news", padx=20, pady=5)

bookingPage.mainloop()
