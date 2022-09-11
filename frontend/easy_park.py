from tkinter import *

from tkinter import messagebox
from turtle import update
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from verify_email import verify_email
from tkinter import filedialog
import datetime
import requests

session = requests.Session() # Creates a session with the backend server
baseURL = 'http://127.0.0.1:8000/' # Base url of the backend server

TitleFont = ("Comic Sans MS", 40, "bold")
TextFont = ("Times", 12)


class EasyPark(Tk):
    def __init__(self):
        Tk.__init__(self)

        # creating a container
        self.eval("tk::PlaceWindow . center")
        self.geometry("600x700")
        self.title("EASY PARK")
        container = Frame(self)
        container.pack(side="top")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, UserPage, SignUpPage, RenterPage, ClientPage, AddParkingPage, ReservationPage, AcctUpdatePage, 
                  AcctDeletePage, ReportPage, SearchingPage, ParkingSpotPage):
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

        # Validate Email and Password for login.
        def validate():
            account = email_entry.get()
            password = pw_entry.get()

            if account == "" or password == "":
                messagebox.showerror('Error', message="Email and Password Can\'t be blank")
                
            data = {'email': email_entry.get(), 'password' : pw_entry.get()}
            res = session.post(baseURL + 'users/signin/', data) # POST Request to authenticate user before logging in

            if(res.json() == "User Logged In"):
                res = session.get(baseURL + 'users/')  # GET Request to retrieve user info after authentication
                controller.frames[UserPage].label.config(text="Welcome " + res.json()['first_name'] + "!") # Update the Welcome Label in UserPage with the user's name
                controller.show_frame(UserPage) # Display UserPage

            elif(res.json() == "Wrong Credentials"):
                messagebox.showerror('Error', message="Incorrect Credentials")
            else:
                messagebox.showerror('Error', message="Something went wrong with backend server!")

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
        self.label = Label(self, text="Welcome!", font=TitleFont)
        self.label.pack(padx=5, pady=5)
        
        def logoff():
            res = session.get(baseURL + 'users/signout/')

            if(res.json() == "Logged out"):
                controller.show_frame(LoginPage) 
            else:
                print("Something went wrong in the backend")

            
        # Renter interface
        renter_button = Button(self, text="Renter", font=TextFont, bg="white", command=lambda: controller.show_frame(RenterPage))
        renter_button.pack(padx=5, pady=20)
        # Client interface
        client_button = Button(self, text="Client", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage))
        client_button.pack(padx=5, pady=20)
        # View Reservation
        edit_button = Button(self, text="View Reservation", bg="white", font=TextFont, command=lambda: controller.show_frame(ReservationPage))
        edit_button.pack(padx=5, pady=20)
        # Update Account
        edit_button = Button(self, text="Update Account", bg="white", font=TextFont, command=lambda: controller.show_frame(AcctUpdatePage))
        edit_button.pack(padx=5, pady=20)
        # Delete Account
        delete_button = Button(self, text="Delete Account", bg="white", font=TextFont, command=lambda: controller.show_frame(AcctDeletePage))
        delete_button.pack(padx=5, pady=20)
        # Monthly Report
        delete_button = Button(self, text="Monthly Report", bg="white", font=TextFont, command=lambda: controller.show_frame(ReportPage))
        delete_button.pack(padx=5, pady=20)
        # Log Off
        logoff_button = Button(self, text="Log Off", font=TextFont, bg="white", command=logoff) 
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

        # Location
        Label(self, text="Location: ", font=TextFont).grid(row=3, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=3, column=1)

        # Vehicle Type
        Label(self, text="Vehicle Type: ", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        v_type.set("Compact")
        vehicle_type1 = Radiobutton(self, text="Compact", variable=v_type, value="Compact", font=TextFont)
        vehicle_type1.grid(row=5, column=1, sticky="w")
        vehicle_type2 = Radiobutton(self, text="Standard", variable=v_type, value="Standard", font=TextFont)
        vehicle_type2.grid(row=5, column=2, sticky="w")
        vehicle_type3 = Radiobutton(self, text="SUV", variable=v_type, value="SUV", font=TextFont)
        vehicle_type3.grid(row=6, column=1, pady=5, sticky="w")
        vehicle_type4 = Radiobutton(self, text="Oversize", variable=v_type, value="Oversize", font=TextFont)
        vehicle_type4.grid(row=6, column=2, sticky="w")

        def loadSearchPage():
            res = session.get(baseURL + 'parking/')

            if(len(res.json()) == 1 ):
                controller.frames[SearchingPage].location1.config(text="Location: " + res.json()[0]['street_address']+", " + res.json()[0]['city']+", " + res.json()[0]['state'] + " " + res.json()[0]['zip_code'] 
                + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0]['end_date']  )

                if(res.json()[0]['image'] != None):
                    controller.frames[SearchingPage].garage1.config(image=res.json()[0]['image'])

                controller.show_frame(SearchingPage)
            elif( len(res.json()) == 2):
                controller.frames[SearchingPage].location1.config(text="Location: " + res.json()[0]['street_address']+", " + res.json()[0]['city']+", " + res.json()[0]['state'] + " " + res.json()[0]['zip_code'] 
                + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0]['end_date']  )
                controller.frames[SearchingPage].location2.config(text="Location: " + res.json()[1]['street_address']+", " + res.json()[1]['city']+", " + res.json()[1]['state'] + " " + res.json()[1]['zip_code'] 
                + "\n" + "Time: " + res.json()[1]['start_date'] + "-" + res.json()[1]['end_date']  )
                controller.show_frame(SearchingPage)

                if(res.json()[0]['image'] != None):
                    controller.frames[SearchingPage].garage1.config(image=res.json()[0]['image'])
                if(res.json()[1]['image'] != None):
                    controller.frames[SearchingPage].garage2.config(image=res.json()[1]['image'])
                 
            else:
                messagebox.showerror("No Parking Spot Found", message="Change search parameters and try again")


        Button(self, text="Search", font=TextFont, bg="white", command=loadSearchPage).grid(row=7, column=0, pady=15, sticky="e")
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).grid(row=7, column=2, pady=15, sticky="w")


# Renter - Searching Page
class SearchingPage(Frame):
       def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Available Parking", font=TitleFont)
        label.grid(row=0, column=0, columnspan= 2, pady=15)

        def reserve():
            messagebox.showinfo(title="Success", message="Your parking spot is successfully reserved.")
            controller.show_frame(UserPage)

        address1 = "Lyon St, San Francisco, CA 94123"
        address2 = "Lombard St, San Francisco, CA 94123"

        availabletime1 = "09/04/2022 00:00 - 09/08/2022 00:00"
        availabletime2 = "09/04/2022 12:00 - 09/10/2022 12:00"
        
        hourly_rate = "$1.50/hrs"

        garage1 = Image.open("no_image.png").resize((200, 150))
        garage1_img = ImageTk.PhotoImage(garage1)

        garage2 = Image.open("no_image.png").resize((200, 150))
        garage2_img = ImageTk.PhotoImage(garage2)
        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]
        start_clicked = StringVar()
        start_clicked.set(time_option[0])
        end_clicked = StringVar()
        end_clicked.set(time_option[0])

        # Parking Garage 1
        garage = Label(self, image=garage1_img)
        garage.image = garage1_img
        garage.grid(row=1, column=0, pady=15)
        start_time1 = OptionMenu(self, start_clicked, *time_option)
        start_time1.grid(row=1, column=1)
        Label(self, text="to    ").grid(row=1, column=2)
        end_time1 = OptionMenu(self, end_clicked, *time_option)
        end_time1.grid(row=1, column=3)
        Label(self, text="Location: " + address1 + "\n" + "Time: " + availabletime1 + "\n" + "Hours Rate: " + hourly_rate).grid(row=2, column=0, sticky="w")
        reserve1 = Button(self, text="Reserve", command=reserve)
        reserve1.grid(row=2, column=1, pady=15, columnspan=3)

        # Parking Garage 2
        garage = Label(self, image=garage2_img)
        garage.image = garage2_img
        garage.grid(row=3, column=0, pady=15)
        start_time1 = OptionMenu(self, start_clicked, *time_option)
        start_time1.grid(row=3, column=1)
        Label(self, text="to    ").grid(row=3, column=2)
        end_time1 = OptionMenu(self, end_clicked, *time_option)
        end_time1.grid(row=3, column=3)
        Label(self, text="Location: " + address2 + "\n" + "Time: " + availabletime2 + "\n" + "Hours Rate: " + hourly_rate).grid(row=4, column=0, sticky="w")
        reserve2 = Button(self, text="Reserve", command=reserve)
        reserve2.grid(row=4, column=1, pady=15, columnspan=3)

        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(ReservationPage)).grid(row=5, column=0, pady=15, columnspan=3)

# Renter - Searching Page
"""class SearchingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Find Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=15)"""


# Client Page
class ClientPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Find Parking Spot", font=TitleFont)
        label.pack(pady=20)

        Button(self, text="Add Parking Spot", font=TextFont, bg="white", command=lambda: controller.show_frame(AddParkingPage)).pack(pady=20)
        Button(self, text="View Parking Spot", font=TextFont, bg="white").pack(pady=20)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).pack(pady=20)


# Client - Add Parking Page
class AddParkingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Add Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        clicked_start = StringVar()
        clicked_start.set(time_option[0])
        
        clicked_end = StringVar()
        clicked_end.set(time_option[0])


        filename = StringVar()

        def added():
            # When doing post requests we need to retrieve the csrftoken with a GET request then we can do a POST request

            res = session.get(baseURL + "parking/") # Retriveing csrftoken 
            csrftoken = res.cookies['csrftoken']
            # using csrftoken in POST request
            data = {'csrfmiddlewaretoken': csrftoken,  'image': img, 'street_address' : street_entry.get().lower(), 'city' : city_entry.get().lower(), 'state' : state_entry.get().lower(), 'zip_code' : zipcode_entry.get(), 'vehicle_type' : v_type.get().lower(), 'start_date': start_cal.get_date(), 'start_time': clicked_start.get(),  'end_date' : end_cal.get_date(), 'end_time': clicked_end.get()}
            res = session.post(baseURL + "parking/", data=data)
            if(res.json() == "New Spot Created"):
                messagebox.showinfo(messagebox.showinfo(title="Success", message="Successfully Added Parking Sot"))
                controller.show_frame(ParkingSpotPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")


        def save_png():
            try:
                global img
                filetypes = [("PNG", "*.png"), ("JPG", "*.jpg"), ('All files', '*')]
                filepath = filedialog.askopenfilename(title='Open files', initialdir='C:/Users/Administrator/Desktop', filetypes=filetypes, defaultextension='.jpg')
                filename.set(filepath)
                print(filepath)
                print(filepath)
                print(filename.get())

                img = Image.open(filename.get())

                # filenewpath = filedialog.asksaveasfilename(title='upload', filetypes=filetypes, defaultextension='.png', initialdir='C:/Users/Administrator/Desktop')
                # path_var.set(filenewpath)
                # img.save(str(path_var.get()))
            except Exception as e:
                print(e)

        v_type = StringVar()

        # Start Date & Time
        Label(self, text="Start Day & Time:", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked_start, *time_option)
        start_time.grid(row=1, column=2)

        # End Date & Time
        Label(self, text="End Day & Time:", font=TextFont).grid(row=2, column=0, pady=15, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked_end, *time_option)
        end_time.grid(row=2, column=2)

        # Location - Street, City, State, Zipcode
        #Label(self, text="House #: ", font=TextFont).grid(row=3, column=0, pady=15, sticky="e")
        #house_entry = Entry(self, font=TextFont)
        #house_entry.grid(row=3, column=1)
        Label(self, text="Street: ", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        street_entry = Entry(self, font=TextFont)
        street_entry.grid(row=4, column=1)
        Label(self, text="City: ", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=5, column=1)
        Label(self, text="State: ", font=TextFont).grid(row=6, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=6, column=1)
        Label(self, text="Zip Code: ", font=TextFont).grid(row=7, column=0, pady=15, sticky="e")
        zipcode_entry = Entry(self, font=TextFont)
        zipcode_entry.grid(row=7, column=1)

        # Vehicle Type
        Label(self, text="Vehicle Type Fit In Garage: ", font=TextFont).grid(row=8, column=0, pady=15, sticky="e")
        v_type.set("Compact")
        vehicle_type1 = Radiobutton(self, text="Compact", variable=v_type, value="Compact", font=TextFont)
        vehicle_type1.grid(row=8, column=1, sticky="w")
        vehicle_type2 = Radiobutton(self, text="Standard", variable=v_type, value="Standard", font=TextFont)
        vehicle_type2.grid(row=8, column=2, sticky="w")
        vehicle_type3 = Radiobutton(self, text="SUV", variable=v_type, value="SUV", font=TextFont)
        vehicle_type3.grid(row=9, column=1, pady=5, sticky="w")
        vehicle_type4 = Radiobutton(self, text="Oversize", variable=v_type, value="Oversize", font=TextFont)
        vehicle_type4.grid(row=9, column=2, sticky="w")

        # Upload image
        Label(self, text="Image: ", font=TextFont).grid(row=10, column=0, pady=15, sticky="e")
        # Button(self, text="image path", command=open_img).grid(row=7, column=1, pady=15)
        Button(self, text="upload", font=TextFont, command=save_png, bg="white").grid(row=10, column=1, pady=15)

        Button(self, text="Add", font=TextFont, bg="white", command=added).grid(row=11, column=2, pady=15)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage)).grid(row=11, column=0, pady=15, sticky="w")
        
# Client - Parking Spot
class ParkingSpotPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=2)

        address1 = "Lyon St, San Francisco, CA 94123"
        availabletime1 = "09/04/2022 00:00 - 09/08/2022 00:00"

        #garage1 = Image.open("no image.jpg").resize((200, 150))
        #garage1_img = ImageTk.PhotoImage(garage1)

        #garage = Label(self, image=garage1_img)
        #garage.image = garage1_img
        #garage.grid(row=1, column=0, pady=15, columnspan=2)
        Label(self, text="Location: " + address1 + "\n" + "Time: " + availabletime1).grid(row=2, column=0, columnspan=2)

        Button(self, text="edit", font=TextFont, bg="white").grid(row=3, column=0, pady=15)
        Button(self, text="delete", font=TextFont, bg="white").grid(row=3, column=1, pady=15)

        Button(self, text="back", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage)).grid(row=4, column=0, pady=15, columnspan=2)

        
# Reservation page
class ReservationPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Reservation", font=TitleFont)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        address1 = "Lyon St, San Francisco, CA 94123"
        availabletime1 = "09/04/2022 00:00 - 09/08/2022 00:00"
        total = "$20.75"

        #garage1 = Image.open("no image.jpg").resize((200, 150))
        #garage1_img = ImageTk.PhotoImage(garage1)

        #garage = Label(self, image=garage1_img)
        #garage.image = garage1_img
        #garage.grid(row=1, column=0, pady=15, columnspan=2)
        Label(self, text="Location: " + address1 + "\n" + "Time: " + availabletime1 + "\n" + "Total: " + total).grid(row=2, column=0, columnspan=2)

        Button(self, text="modify", font=TextFont, bg="white").grid(row=3, column=0, pady=15)
        Button(self, text="cancel", font=TextFont, bg="white").grid(row=3, column=1, pady=15)

        Button(self, text="back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).grid(row=4, column=0, pady=15, columnspan=2)

        
# Client - Parking Spot
class ParkingSpotPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Find Parking Spot", font=TitleFont)
        label.pack(pady=20)
        
        
# Update Account page
class AcctUpdatePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Update", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        Label(self, text="*Please fill in what you would like to update:", font=("Times", 15)).grid(row=1, column=0, columnspan=2, pady=5, sticky="nw")

        def update():
            if firstname != "":
                new_firstname = firstname
            if lastname != "":
                new_lastname = lastname
            if email != "":
                new_email = email
            if phone != "":
                new_phone = phone
            if password != "":
                new_password = password
            if bank != "":
                new_bank = bank
            if routing != "":
                new_routing = routing
            if account != "":
                new_account = account
            controller.show_frame(UserPage)

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
        pw_entry = Entry(self, font=TextFont)
        pw_entry.grid(row=6, column=1, sticky="w")

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

        Button(self, text="Confirm Update", font=TextFont, bg="white", command=update).grid(row=11, column=0)

        Button(self, text="Back", command=lambda: controller.show_frame(UserPage), font=TextFont).grid(row=11, column=1, padx=10, pady=10)

        # Getter
        firstname = fn_entry.get()
        lastname = ln_entry.get()
        email_input = email_entry.get()
        email = verify_email(email_input)
        phone = phone_entry.get()
        password = pw_entry.get()
        bank = bank_entry.get()
        routing = routing_entry.get()
        account = account_entry.get()


# Delete Account page
class AcctDeletePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Delete Account", font=TitleFont)
        label.pack(pady=20)

        Button(self, text="Confirm Delete", font=TextFont, bg="white", command=lambda: controller.show_frame(LoginPage)).pack(pady=20)
        Button(self, text="Back", command=lambda: controller.show_frame(UserPage), font=TextFont).pack(pady=20)


# Monthly Report Page
class ReportPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Monthly Report", font=TitleFont)
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label = Label(self, text="There are no reports for your account at this time.", font=TextFont)
        label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        label = Label(self, text="Please check back next month!", font=TextFont)
        label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).grid(row=3, column=0, pady=20)


# Sign Up Page
class SignUpPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Sign Up", font=TitleFont)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

        def verifyAcc():

            if not fn_entry.get() or not ln_entry.get() or not email_entry.get() or not phone_entry.get() or not pw_entry.get() or not confirm_entry.get() or not bank_entry.get() or not routing_entry.get() or not account_entry.get(): 
                messagebox.showerror('Error', message='Please fill in all info!')
                if password != confirm:
                    messagebox.showerror('Error', message='Password and confirm password must be the same!')
                    if type(phone) != int and len(phone) != 10:
                        messagebox.showerror('Error', message='Phone Number enter is increase!')
                        if not email_verify:
                            messagebox.showerror('Error', message='Email enter is increase!')
            else:
                
                data = {'first_name' : fn_entry.get(), 'last_name': ln_entry.get(), 'email': email_entry.get(), 'password' : pw_entry.get()}
                res = session.post(baseURL + 'users/signup/', data)
                
                if(res.json() == "New User Created"):
                    messagebox.showinfo(title="Success", message="Successfully Signed Up")
                    controller.show_frame(LoginPage) 
                else:
                    print("Something went wrong in the backend")


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
