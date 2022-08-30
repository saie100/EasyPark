from tkinter import *
from tkinter import messagebox
from verify_email import verify_email
from tkcalendar import DateEntry
from geopy.geocoders import Nominatim
import requests

TitleFont = ("Castellar", 50, "bold")
TextFont = ("Times New Roman", 12)


class EasyPark(Tk):
    def __init__(self):
        Tk.__init__(self)

        # creating a container
        self.geometry("600x700")
        self.title("EASY PARK")
        container = Frame(self)
        container.pack(side="top")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, Page1, SignUpPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Title - Easy Park
        title_label = Label(self, text="Easy\nPark", font=TitleFont)
        title_label.pack(padx=10, pady=10)

        # Slogan
        slogan_label = Label(self, text="Make Parking Easier", font=("Tempus Sans ITC", 15))
        slogan_label.pack(padx=10, pady=10)

        # Email Entry
        Label(self, text="Email:", fg="black", border=0, font=TextFont).pack(padx=5, pady=5)
        Entry(self, font=TextFont).pack(padx=5, pady=5)

        Label(self, text="Password: ", fg="black", border=0, font=TextFont).pack(padx=5, pady=5)
        Entry(self, show="*", font=TextFont).pack(padx=5, pady=5)

        button1 = Button(self, text="Log In", font=TextFont, command=lambda: controller.show_frame(Page1))
        button1.pack(side=LEFT)
        button2 = Button(self, text="Sign Up", font=TextFont, command=lambda: controller.show_frame(SignUpPage))
        button2.pack(side=RIGHT)


# second window frame page1
class Page1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Search", font=TitleFont)
        label.grid(row=0, column=0, columnspan= 3, padx=10, pady=10)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        clicked = StringVar()
        clicked.set(time_option[0])

        Label(self, text="Start Day & Time:", font=TextFont).grid(row=1, column=0, pady=5, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked, *time_option)
        start_time.grid(row=1, column=2)

        Label(self, text="End Day & Time:", font=TextFont).grid(row=2, column=0, pady=5, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked, *time_option)
        end_time.grid(row=2, column=2)

        Label(self, text="Zipcode:", font=TextFont).grid(row=3, column=0, pady=5, sticky="e")
        zipcode_entry = Entry(self, font=TextFont)
        zipcode_entry.grid(row=3, column=1, pady=5)
        zipcode_input = zipcode_entry.get()

        # Button(self, text="LookUp", command=LookupLocation())

        Label(self, text="Location:", font=("Comic Sans MS", 12)).grid(row=4, column=0, pady=5, sticky="e")
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(zipcode_input)

        button1 = Button(self, text="Search", command=lambda: controller.show_frame(LoginPage))
        button1.grid(row=10, column=0, columnspan= 3, padx=10, pady=10)



class SignUpPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Sign Up", font=TitleFont)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        def verifyAcc():
            if not fn_entry.get() and not ln_entry.get() and not email_entry.get() and not phone_entry.get() and \
                    not pw_entry.get() and not confirm_entry.get() and not bank_entry.get() and not routing_entry.get() \
                    and not account_entry.get():
                messagebox.showerror('Error', message='Please fill in all info!')
                if password != confirm:
                    messagebox.showerror('Error', message='Password and confirm password must be the same!')
                    if type(phone) != int and len(phone) != 10:
                        messagebox.showerror('Error', message='Phone Number enter is increase!')
                        if not email:
                            messagebox.showerror('Error', message='Email enter is increase!')
            else:
                
                url = 'http://127.0.0.1:8000/users/signup/'
                data = {'first_name': 'Greg', 'last_name' : 'Kent', 'username': 'gk', 'email': 'gk@yahoo.com', 'password': '123' }
                response = requests.post(url , data)

                response = requests.get('http://127.0.0.1:8000/users/')
                
                print(response.json())
                messagebox.showinfo(title="Success", message="Successfully Signed Up")

        r = StringVar()

        Label(self, text="*Please fill in this form to create an account:", font=("Comic Sans MS", 15)).grid(row=1, column=0, columnspan=2, pady=5, sticky="nw")

        # First Name
        Label(self, text="First Name:", font=TextFont).grid(row=2, column=0, pady=5, sticky="e")
        fn_entry = Entry(self, font=TextFont)
        fn_entry.grid(row=2, column=1, sticky="w")

        # Last Name
        Label(self, text="Last Name:", font=TextFont).grid(row=3, column=0, pady=5, sticky="e")
        ln_entry = Entry(self, font=TextFont)
        ln_entry.grid(row=3, column=1, sticky="w")

        # Email
        Label(self, text="Email Address:", font=TextFont).grid(row=4, column=0, pady=5, sticky="e")
        email_entry = Entry(self, font=TextFont)
        email_entry.grid(row=4, column=1, sticky="w")

        # Phone Number
        Label(self, text="Phone#:", font=TextFont).grid(row=5, column=0, pady=5, sticky="e")
        phone_entry = Entry(self, font=("Comic Sans MS", 10))
        phone_entry.grid(row=5, column=1, sticky="w")

        # Password
        Label(self, text="Password:", font=TextFont).grid(row=6, column=0, pady=5, sticky="e")
        pw_entry = Entry(self, show="*", font=TextFont)
        pw_entry.grid(row=6, column=1, sticky="w")

        # Password Confirm
        Label(self, text="Confirm Password:", font=TextFont).grid(row=7, column=0, pady=5,sticky="e")
        confirm_entry = Entry(self, show="*", font=TextFont)
        confirm_entry.grid(row=7, column=1, sticky="w")

        # Renter or Client selection
        Label(self, text="Account Type:", font=TextFont).grid(row=8, column=0, pady=5, sticky="e")
        Radiobutton(self, text="Renter", variable=r, value='Renter', font=TextFont).grid(row=9, column=0, pady=5, sticky="e")
        Radiobutton(self, text="Client", variable=r, value='Client', font=TextFont).grid(row=9, column=1, pady=5)

        # Bank Info
        Label(self, text="Bank Name: ", font=TextFont).grid(row=10, column=0, pady=5, sticky="e")
        bank_entry = Entry(self, font=TextFont)
        bank_entry.grid(row=10, column=1, sticky="w")

        # Routing Number
        Label(self, text="Routing Number: ", font=TextFont).grid(row=11, column=0, sticky="e")
        routing_entry = Entry(self, font=TextFont)
        routing_entry.grid(row=11, column=1, sticky="w")

        # Account Number
        Label(self, text="Account Number: ", font=TextFont).grid(row=12, column=0, pady=5, sticky="e")
        account_entry = Entry(self, font=TextFont)
        account_entry.grid(row=12, column=1, sticky="w")

        # Getter
        password = pw_entry.get()
        confirm = confirm_entry.get()

        phone = phone_entry.get()

        email_input = email_entry.get()
        email = verify_email(email_input)

        Button(self, text="Confirm", command=verifyAcc, font=TextFont).grid(row=13, column=0, pady=30, sticky="e")
        Button(self, text="Login", command=lambda: controller.show_frame(LoginPage), font=TextFont).grid(row=13, column=1)


# Driver Code
app = EasyPark()
app.mainloop()
