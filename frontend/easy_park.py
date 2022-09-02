from tkinter import *
from tkinter import messagebox
from verify_email import verify_email
from tkcalendar import DateEntry
from PIL import ImageTk, Image

TitleFont = ("Comic Sans MS", 40, "bold")
TextFont = ("Times", 12)


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

        for F in (LoginPage, UserPage, SignUpPage, RenterPage, ClientPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Main page - sign in
class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def validate():
            account = email_entry.get()
            password = pw_entry.get()
            if account == "" or password == "":
                messagebox.showerror('Error', message="Email and Password Can\'t be blank")
            elif account == "cse682" and password == "cse682":
                controller.show_frame(UserPage)
            else:
                messagebox.showerror('Error', message="Incorrect Account and Password")

        # Title - Easy Park
        title_label = Label(self, text="Easy Park", font=TitleFont)
        title_label.pack(padx=10, pady=10)

        # Logo Image
        logo = Image.open("logo.png")
        logo_resize = logo.resize((150, 150))
        logo_img = ImageTk.PhotoImage(logo_resize)
        logo_label = Label(self, image=logo_img)
        logo_label.image = logo_img
        logo_label.pack()

        # Slogan
        slogan_label = Label(self, text="Make Parking Easier", font=("Tempus Sans ITC", 15))
        slogan_label.pack(padx=10, pady=10)

        # Email Entry
        Label(self, text="Email:", fg="black", border=0, font=TextFont).pack(padx=5, pady=5)
        email_entry = Entry(self, font=TextFont)
        email_entry.pack(padx=5, pady=5)

        Label(self, text="Password: ", fg="black", border=0, font=TextFont).pack(padx=5, pady=5)
        pw_entry = Entry(self, show="*", font=TextFont)
        pw_entry.pack(padx=5, pady=5)

        button1 = Button(self, text="Log In", font=TextFont, bg="white", command=validate)
        button1.pack(side=RIGHT)
        button2 = Button(self, text="Sign Up", font=TextFont, bg="white", command=lambda: controller.show_frame(SignUpPage))
        button2.pack(side=LEFT)


# User Page - after signing in
class UserPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Welcome", font=TitleFont)
        label.pack(padx=5, pady=5)
        # Renter interface
        renter_button = Button(self, text="Renter", font=TextFont, bg="white", command=lambda: controller.show_frame(RenterPage))
        renter_button.pack(padx=5, pady=20)
        # Client interface
        client_button = Button(self, text="Client", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage))
        client_button.pack(padx=5, pady=20)
        # Account update
        update_button = Button(self, text="Update Account", bg="white", font=TextFont)
        update_button.pack(padx=5, pady=20)
        # Delete Account
        delete_button = Button(self, text="Delete Account", bg="white", font=TextFont)
        delete_button.pack(padx=5, pady=20)
        # Log Off
        logoff_button = Button(self, text="Log Off", font=TextFont, bg="white", command=lambda: controller.show_frame(LoginPage))
        logoff_button.pack(padx=5, pady=20)


# Renter Page
class RenterPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Find Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=15)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        clicked = StringVar()
        clicked.set(time_option[0])

        v_type = StringVar()

        # Start Date & Time
        Label(self, text="Start Day & Time:", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked, *time_option)
        start_time.grid(row=1, column=2)

        # End Date & Time
        Label(self, text="End Day & Time:", font=TextFont).grid(row=2, column=0, pady=15, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked, *time_option)
        end_time.grid(row=2, column=2)

        # Location - City
        Label(self, text="City: ", font=TextFont).grid(row=3, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=3, column=1)

        # Location - State
        Label(self, text="State: ", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=4, column=1)

        # Vehicle Type
        Label(self, text="Vehicle Type: ", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        v_type.set("Compact")
        vehicle_type1 = Radiobutton(self, text="Compact", variable=v_type, value="Compact")
        vehicle_type1.grid(row=5, column=1, sticky="w")
        vehicle_type2 = Radiobutton(self, text="Standard", variable=v_type, value="Standard")
        vehicle_type2.grid(row=5, column=2, sticky="w")
        vehicle_type3 = Radiobutton(self, text="SUV", variable=v_type, value="SUV")
        vehicle_type3.grid(row=6, column=1, pady=5, sticky="w")
        vehicle_type4 = Radiobutton(self, text="Oversize", variable=v_type, value="Oversize")
        vehicle_type4.grid(row=6, column=2, sticky="w")

        Button(self, text="Search", font=TextFont, bg="white").grid(row=7, column=0, pady=15, sticky="e")
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).grid(row=7, column=2, pady=15, sticky="w")


# Client Page
class ClientPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Add Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        clicked = StringVar()
        clicked.set(time_option[0])

        v_type = StringVar()

        # Start Date & Time
        Label(self, text="Start Day & Time:", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked, *time_option)
        start_time.grid(row=1, column=2)

        # End Date & Time
        Label(self, text="End Day & Time:", font=TextFont).grid(row=2, column=0, pady=15, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked, *time_option)
        end_time.grid(row=2, column=2)

        # Location - City
        Label(self, text="City: ", font=TextFont).grid(row=3, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=3, column=1)

        # Location - State
        Label(self, text="State: ", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=4, column=1)

        # Vehicle Type
        Label(self, text="Vehicle Type: ", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        v_type.set("Compact")
        vehicle_type1 = Radiobutton(self, text="Compact", variable=v_type, value="Compact")
        vehicle_type1.grid(row=5, column=1, sticky="w")
        vehicle_type2 = Radiobutton(self, text="Standard", variable=v_type, value="Standard")
        vehicle_type2.grid(row=5, column=2, sticky="w")
        vehicle_type3 = Radiobutton(self, text="SUV", variable=v_type, value="SUV")
        vehicle_type3.grid(row=6, column=1, pady=5, sticky="w")
        vehicle_type4 = Radiobutton(self, text="Oversize", variable=v_type, value="Oversize")
        vehicle_type4.grid(row=6, column=2, sticky="w")

        Button(self, text="Search", font=TextFont).grid(row=7, column=0, columnspan=3, pady=15)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).grid(row=7, column=2, pady=15, sticky="w")


# Sign Up Page
class SignUpPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Sign Up", font=TitleFont)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        def verifyAcc():
            if firstname == "" or lastname == "" or email == "" or phone == "" or password == "" or confirm == "" or bank == "" or routing == "" or account == "":
                messagebox.showerror('Error', message='Please fill in all info!')
                if password != confirm:
                    messagebox.showerror('Error', message='Password and confirm password must be the same!')
                    if type(phone) != int and len(phone) != 10:
                        messagebox.showerror('Error', message='Phone Number enter is increase!')
                        if not email_verify:
                            messagebox.showerror('Error', message='Email enter is increase!')
            else:
                messagebox.showinfo(title="Success", message="Successfully Signed Up")

        Label(self, text="*Please fill in this form to create an account:", font=("Times", 15)).grid(row=1, column=0, columnspan=2, pady=5, sticky="nw")

        # First Name
        Label(self, text="First Name:*", font=TextFont).grid(row=2, column=0, pady=5, sticky="e")
        fn_entry = Entry(self, font=TextFont)
        fn_entry.grid(row=2, column=1, sticky="w")

        # Last Name
        Label(self, text="Last Name:*", font=TextFont).grid(row=3, column=0, pady=5, sticky="e")
        ln_entry = Entry(self, font=TextFont)
        ln_entry.grid(row=3, column=1, sticky="w")

        # Email
        Label(self, text="Email Address:*", font=TextFont).grid(row=4, column=0, pady=5, sticky="e")
        email_entry = Entry(self, font=TextFont)
        email_entry.grid(row=4, column=1, sticky="w")

        # Phone Number
        Label(self, text="Phone#:*", font=TextFont).grid(row=5, column=0, pady=5, sticky="e")
        phone_entry = Entry(self, font=("Comic Sans MS", 10))
        phone_entry.grid(row=5, column=1, sticky="w")

        # Password
        Label(self, text="Password:*", font=TextFont).grid(row=6, column=0, pady=5, sticky="e")
        pw_entry = Entry(self, show="*", font=TextFont)
        pw_entry.grid(row=6, column=1, sticky="w")

        # Password Confirm
        Label(self, text="Confirm Password:*", font=TextFont).grid(row=7, column=0, pady=5, sticky="e")
        confirm_entry = Entry(self, show="*", font=TextFont)
        confirm_entry.grid(row=7, column=1, sticky="w")

        # Bank Info
        Label(self, text="Bank Name:*", font=TextFont).grid(row=8, column=0, pady=5, sticky="e")
        bank_entry = Entry(self, font=TextFont)
        bank_entry.grid(row=8, column=1, sticky="w")

        # Routing Number
        Label(self, text="Routing Number:*", font=TextFont).grid(row=9, column=0, sticky="e")
        routing_entry = Entry(self, font=TextFont)
        routing_entry.grid(row=9, column=1, sticky="w")

        # Account Number
        Label(self, text="Account Number:*", font=TextFont).grid(row=10, column=0, pady=5, sticky="e")
        account_entry = Entry(self, font=TextFont)
        account_entry.grid(row=10, column=1, sticky="w")

        # Getter
        firstname = fn_entry.get()
        lastname = ln_entry.get()
        email = email_entry.get()
        email_verify = verify_email(email)
        phone = phone_entry.get()
        password = pw_entry.get()
        confirm = confirm_entry.get()
        bank = bank_entry.get()
        routing = routing_entry.get()
        account = account_entry.get()

        Button(self, text="Confirm", command=verifyAcc, font=TextFont).grid(row=13, column=0, pady=30, sticky="e")
        Button(self, text="Login", command=lambda: controller.show_frame(LoginPage), font=TextFont).grid(row=13, column=1)


# Driver Code
app = EasyPark()
app.mainloop()
