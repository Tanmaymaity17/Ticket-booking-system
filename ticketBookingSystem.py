import tkinter
import tkinter as tk
from tkcalendar import Calendar
from firebase_admin import db, credentials, initialize_app
from subprocess import call
from PIL import Image, ImageTk

# Initialize Firebase
cred = credentials.Certificate("python-ticket-booking-firebase.json")
initialize_app(cred, {"databaseURL": "https://python-ticket-booking-default-rtdb.firebaseio.com/"})
database_ref = db.reference("/users")


source_entry = ''
destination_entry = ''
date_entry = ''


def open_train_database(source, destination, date):
    call(["python", "trains_database.py", source, destination, date])


def open_flight_database(source, destination, date):
    call(["python", "flights_database.py", source, destination, date])


# Create a Tkinter window
login_page = tk.Tk()
login_page.title("Login Page")
login_page.configure(bg='#1d91cc')

login_image = tk.PhotoImage(file="loginpage-background.png")
login_label = tk.Label(login_page, image=login_image)
login_label.image = login_image
login_label.place(x=0, y=0, relwidth=1, relheight=1)

frame_login = tkinter.Frame(login_page)
frame_login.pack(padx=20, pady=10)
frame_login.configure(bg='#1d91cc')

# Global variable to store the selected transport mode
transport_mode = None


def open_homepage():
    login_page.destroy()  # Close the login window

    global source_entry, destination_entry, date_entry

    def search_transport(mode):
        source = source_entry.get()
        destination = destination_entry.get()
        date = date_entry.get()

        print(source + destination + date)

        if mode == 1:
            print("Search for airplanes")
            homepage.destroy()
            # Add your logic to search for airplanes

            open_flight_database(str(source), str(destination), str(date))
        elif mode == 0:
            print("Search for trains")
            homepage.destroy()
            # Add your logic to search for trains

            open_train_database(str(source), str(destination), str(date))

    def select_date():
        def set_selected_date():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, cal.selection_get().strftime('%Y-%m-%d'))
            top.destroy()

        top = tk.Toplevel(homepage)
        cal = Calendar(top, selectmode='day')
        cal.pack()
        select_button = tk.Button(top, text="Select", command=set_selected_date)
        select_button.pack()

    def set_airplane_mode():
        global transport_mode
        transport_mode = 1

    def set_train_mode():
        global transport_mode
        transport_mode = 0

    # Create and run the homepage window
    homepage = tk.Tk()
    homepage.title("Airline and Train Ticket Booking System")
    homepage.configure(bg='#1d91cc')

    frame_home = tkinter.Frame(homepage)
    frame_home.pack(padx=20, pady=10)
    frame_home.configure(bg='#1d91cc')

    # Entry fields for source, destination, and date
    source_label = tk.Label(frame_home, text="Source:", bg='#105274', fg='#FFFFFF', font='Arial')
    source_label.grid(row=0, column=0, sticky="e")
    source_entry = tk.Entry(frame_home, font='Arial')
    source_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    destination_label = tk.Label(frame_home, text="Destination:", bg='#105274', fg='#FFFFFF', font='Arial')
    destination_label.grid(row=1, column=0, sticky="e")
    destination_entry = tk.Entry(frame_home, font='Arial')
    destination_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    date_label = tk.Label(frame_home, text="Date:", bg='#105274', fg='#FFFFFF', font='Arial')
    date_label.grid(row=2, column=0, sticky="e")
    date_entry = tk.Entry(frame_home, font='Arial')
    date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    date_entry.insert(0, "DD-MM-YYYY")
    calendar_button = tk.Button(frame_home, text="📅", command=select_date)
    calendar_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    # Load PNG images
    airplane_image = tk.PhotoImage(file="flight_logo.png")
    train_image = tk.PhotoImage(file="train_logo.png")

    # Add image buttons
    airplane_button = tk.Button(frame_home, image=airplane_image, command=set_airplane_mode)
    airplane_button.grid(row=3, column=0, padx=5, pady=5)
    train_button = tk.Button(frame_home, image=train_image, command=set_train_mode)
    train_button.grid(row=3, column=1, padx=5, pady=5)

    # Button for search
    search_button = tk.Button(frame_home, text="Search", bg='#d4e9f0', fg='#1c120c', font='Arial',
                              command=lambda: search_transport(transport_mode))
    search_button.grid(row=4, columnspan=2, padx=5, pady=5)

    # Run the Tkinter event loop
    homepage.mainloop()


# Function to handle login button click
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check login credentials against the database
    user_data = database_ref.child(username).get()

    if user_data and user_data.get("password") == password:
        success_window = tk.Toplevel(login_page)
        success_window.title("Success")
        label_status.config(text="Login successful!", fg="green", font='Arial')

        # Open the homepage after successful login
        open_homepage()

    else:
        label_status.config(text="Invalid username or password", fg="red", font='Arial')


def logout():
    success_window = tk.Toplevel(login_page)
    success_window.title("Success")
    button_logout = tk.Button(login_page, text="Logout", font='Arial', command=logout)
    button_logout.grid(row=5, column=0, columnspan=2, pady=10)
    label_status.config(text="Logout successful!", fg="green", font='Arial')


# Function to handle sign up button click
def signup():
    # Create a new window for sign up
    signup_window = tk.Toplevel(login_page)
    signup_window.title("Sign Up")
    signup_window.configure(bg='#1d91cc')

    signup_image = tk.PhotoImage(file="loginpage-background.png")
    signup_label = tk.Label(signup_window, image=signup_image)
    signup_label.image = signup_image
    signup_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame_signup = tkinter.Frame(signup_window)
    frame_signup.pack(padx=20, pady=10)
    frame_signup.configure(bg='#1d91cc')

    # Function to handle sign up confirmation button click
    def confirm_signup():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if new_password == confirm_password:
            # Store the new user in the database
            database_ref.child(new_username).set({"password": new_password})
            label_status.config(text="Registration successful!", fg="green", font='Arial')
            signup_window.destroy()
        else:
            label_signup_status.config(text="Passwords do not match", fg="red", font='Arial')

    # Create and place widgets in the sign-up window

    bg_image1 = Image.open('loginpage-background.png')
    bg_photo1 = ImageTk.PhotoImage(bg_image1)
    bg_label1 = tk.Label(frame_signup, image=bg_photo1)
    bg_label1.image = bg_photo1
    bg_label1.place(x=0, y=0, relwidth=1, relheight=1)

    label_new_username = tk.Label(frame_signup, text="Username:", bg='#105274', fg='#FFFFFF', font='Arial')
    label_new_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_new_username = tk.Entry(frame_signup, font='Arial')
    entry_new_username.grid(row=0, column=1, padx=10, pady=10)

    label_new_password = tk.Label(frame_signup, text="Password:", bg='#105274', fg='#FFFFFF', font='Arial')
    label_new_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    entry_new_password = tk.Entry(frame_signup, show="*", font='Arial')
    entry_new_password.grid(row=1, column=1, padx=10, pady=10)

    label_confirm_password = tk.Label(frame_signup, text="Confirm Password:", bg='#105274', fg='#FFFFFF', font='Arial')
    label_confirm_password.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    entry_confirm_password = tk.Entry(frame_signup, show="*", font='Arial')
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=10)

    button_confirm_signup = tk.Button(frame_signup, text="Sign up", bg='#d4e9f0', fg='#1c120c', font='Arial',
                                      command=confirm_signup)
    button_confirm_signup.grid(row=3, column=0, columnspan=2, pady=10)

    label_signup_status = tk.Label(frame_signup, text="", bg='#1d91cc')
    label_signup_status.grid(row=4, column=0, columnspan=2)


# Create and place widgets in the main window

# Load and display background image
bg_image = Image.open('loginpage-background.png')
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(frame_login, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

label_username = tk.Label(frame_login, text="Username:", bg='#105274', fg='#FFFFFF', font='Arial')
label_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entry_username = tk.Entry(frame_login, font='Arial')
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(frame_login, text="Password:", bg='#105274', fg='#FFFFFF', font='Arial')
label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_password = tk.Entry(frame_login, show="*", font='Arial')
entry_password.grid(row=1, column=1, padx=10, pady=10)

button_login = tk.Button(frame_login, text="Login", bg='#d4e9f0', fg='#1c120c', font='Arial', command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

button_signup = tk.Button(frame_login, text="Sign up", bg='#d4e9f0', fg='#1c120c', font='Arial', command=signup)
button_signup.grid(row=3, column=0, columnspan=2, pady=10)

label_status = tk.Label(frame_login, text="", bg='#1d91cc', fg='#1d91cc')
label_status.grid(row=4, column=0, columnspan=2)

# Start the Tkinter event loop
login_page.mainloop()
