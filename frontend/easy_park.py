from cgitb import text
import email
from email.mime import base
from http.client import CannotSendRequest
from tkinter import *

from tkinter import messagebox
from turtle import update
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from verify_email import verify_email
from tkinter import filedialog
import datetime
import requests

from urllib.request import urlopen
from io import BytesIO

session = requests.Session()  # Creates a session with the backend server
baseURL = 'http://127.0.0.1:8000'  # Base url of the backend server

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

        for F in (LoginPage, AdminPage, AdminControl, UserPage, RenterPage, RenterReservationPage,  ClientPage,  SearchPage, ParkingDisplayPage,
                  AddParkingPage, ParkingSpotPage, ModifySpotPage, ClientReservationPage, AccountPage, ViewAcctPage,
                  AcctUpdatePage, AcctDeletePage, ReportPage, SignUpPage):
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
                
            data = {'email': email_entry.get(), 'password': pw_entry.get()}
            res = session.post(baseURL + '/users/signin/', data)  # POST Request to authenticate user before logging in

            if res.json() == "User Logged In":
                res = session.get(baseURL + '/users/')  # GET Request to retrieve user info after authentication
                controller.frames[UserPage].label.config(text="Welcome " + res.json()['first_name'] + "!")  # Update the Welcome Label in UserPage with the user's name
                controller.show_frame(UserPage)  # Display UserPage

            elif(res.json() == "Admin Logged In"):
                controller.show_frame(AdminPage) # Display AdminPage

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


class AdminPage(Frame):
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        self.label = Label(self, text="Admin Page", font=TitleFont)
        self.label.pack(padx=5, pady=5)
        
        def logoff():
            res = session.get(baseURL + '/users/signout/')

            if(res.json() == "Logged out"):
                controller.show_frame(LoginPage) 
            else:
                messagebox.showerror('Error', message='Something went wrong in the backend')
            
        def loadAdminSetting():

            res = session.get(baseURL + '/parking/admin/')
            if(res.json() == "Hourly rate does not exist"):
                messagebox.showinfo(title="Hourly Rate", message="Hourly rate needs to be set")
                controller.show_frame(AdminControl)
            elif(res.json()['hourly_rate']):
                controller.frames[AdminControl].label1.config(text="Current hourly rate: " + res.json()['hourly_rate'])
                controller.show_frame(AdminControl)
            else:
                messagebox.showerror('Error', message='Something went wrong in the backend')


        # Admin Settings
        setprice = Button(self, text="Set Price", font=TextFont, bg="white", command=loadAdminSetting)
        setprice.pack(padx=5, pady=20)
        # Log Off
        logoff_button = Button(self, text="Log Off", font=TextFont, bg="white", command=logoff) 
        logoff_button.pack(padx=5, pady=20)

class AdminControl(Frame):
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        self.label = Label(self, text="Admin Settings", font=TitleFont)
        self.label.pack(padx=5, pady=5)
        

        def setPrice():
            res = session.get(baseURL + '/parking/admin/') # Retriveing csrftoken 
            csrftoken = res.cookies['csrftoken']
            # using csrftoken in POST request

            data = {'csrfmiddlewaretoken': csrftoken, 'hourly_rate' : self.price_entry.get()}
            res = session.post(baseURL + '/parking/admin/', data=data)

            if(res.json() == "Updated hourly rate"):
                messagebox.showinfo(title="Success!", message="Hourly rate has been updated")
                controller.show_frame(AdminPage)
            elif(res.json() == "Created new hourly rate"):
                messagebox.showinfo(title="Success!", message="Hourly rate has been created")
                controller.show_frame(AdminPage)
            else:
                messagebox.showerror('Error', message='Something went wrong in the backend')



        self.label1 = Label(self, text="Current hourly rate: N/A", font=TextFont)
        self.label1.pack(padx=5, pady=5)

        Label(self, text="Set hourly rate:", fg="black", border=0, font=TextFont).pack(padx=5, pady=5)
        self.price_entry = Entry(self, font=TextFont)
        self.price_entry.pack(padx=5, pady=5)
        
        setprice_btn = Button(self, text="Set Price", font=TextFont, bg="white", command=setPrice)
        setprice_btn.pack(padx=5, pady=20)
        # Back to Admin Page
        back_btn= Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(AdminPage)) 
        back_btn.pack(padx=5, pady=20)

# User Page - after signing in
class UserPage(Frame):
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        self.label = Label(self, text="Welcome!", font=TitleFont)
        self.label.pack(padx=5, pady=5)
        
        def logoff():
            res = session.get(baseURL + '/users/signout/')

            if res.json() == "Logged out":
                controller.show_frame(LoginPage) 
            else:
                messagebox.showerror('Error', message='Something went wrong in the backend')

        # Renter interface
        renter_button = Button(self, text="Renter", font=TextFont, bg="white", command=lambda: controller.show_frame(RenterPage))
        renter_button.pack(padx=5, pady=20)
        # Client interface
        client_button = Button(self, text="Client", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage))
        client_button.pack(padx=5, pady=20)
        # Account interface
        account_button = Button(self, text="Account", font=TextFont, bg="white", command=lambda: controller.show_frame(AccountPage))
        account_button.pack(padx=5, pady=20)
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
        label = Label(self, text="Renter Page", font=TitleFont)
        label.pack(pady=20)

        def loadReservation():
            res = session.get(baseURL + '/parking/reserve/?renter=yes')
            if(len(res.json()) == 0):
                
                garage = Image.open("no_image.png").resize((200, 150))
                garage_img = ImageTk.PhotoImage(garage)

                clientname = "N/A"
                address = "N/A"
                timeseleted = "N/A"
                total = "$0.00"

                controller.frames[RenterReservationPage].resv_label1.config(text="Owner of Parking Spot: " + clientname + "\n" + "Location: " + address + "\n" + "Time Slot: " + timeseleted + "\n" + "Total: " + total)
                controller.frames[RenterReservationPage].resv_label2.config(text="Owner of Parking Spot: " + clientname + "\n" + "Location: " + address + "\n" + "Time Slot: " + timeseleted + "\n" + "Total: " + total)

                controller.frames[RenterReservationPage].garage1.config(image=garage_img)
                controller.frames[RenterReservationPage].garage1.image = garage_img
                controller.frames[RenterReservationPage].garage2.config(image=garage_img)
                controller.frames[RenterReservationPage].garage2.image = garage_img

                controller.frames[RenterReservationPage].parking_spot_id1.set(0)
                controller.frames[RenterReservationPage].parking_spot_id2.set(0)
                
            elif(len(res.json()) == 1):

                controller.frames[RenterReservationPage].resv_label1.config(text="Owner of Parking Spot: " + res.json()[0]['client']['first_name'] + 
                " " + res.json()[0]['client']['last_name'] + "\n" + "Location: " + res.json()[0]['parking_spot']['street_address'] + ", "
                + res.json()[0]['parking_spot']['city'] + ", " + res.json()[0]['parking_spot']['state'] + " " + res.json()[0]['parking_spot']['zip_code'] + 
                "\n" + "Time Slot: " + res.json()[0]['start_date'] + 
                " - " + res.json()[0]['end_date']+ "\n" + "Total: " + "$3.00")

                controller.frames[RenterReservationPage].time_slot1.set(res.json()[0]['start_date'] + 
                " - " + res.json()[0]['end_date'])

                controller.frames[RenterReservationPage].parking_spot_id1.set(res.json()[0]['parking_spot_id'])

                if res.json()[0]['parking_spot']['image'] != None:
                    raw_data = urlopen(baseURL + res.json()[0]['parking_spot']['image']).read()
                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((200, 150), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(im)
                    controller.frames[RenterReservationPage].garage1.config(image=photo)
                    controller.frames[RenterReservationPage].garage1.image = photo

            elif len(res.json()) == 2:
                controller.frames[RenterReservationPage].resv_label1.config(text="Owner of Parking Spot: " + res.json()[0]['client']['first_name'] + 
                " " + res.json()[0]['client']['last_name'] + "\n" + "Location: " + res.json()[0]['parking_spot']['street_address'] + ", "
                + res.json()[0]['parking_spot']['city'] + ", " + res.json()[0]['parking_spot']['state'] + " " + res.json()[0]['parking_spot']['zip_code'] + 
                "\n" + "Time Slot: " + res.json()[0]['start_date'] + 
                " - " + res.json()[0]['end_date']+ "\n" + "Total: " + "$3.00")

                controller.frames[RenterReservationPage].resv_label2.config(text="Owner of Parking Spot: " + res.json()[1]['client']['first_name'] + 
                " " + res.json()[1]['client']['last_name'] + "\n" + "Location: " + res.json()[1]['parking_spot']['street_address'] + ", "
                + res.json()[1]['parking_spot']['city'] + ", " + res.json()[1]['parking_spot']['state'] + " " + res.json()[1]['parking_spot']['zip_code'] + 
                "\n" + "Time Slot: " + res.json()[1]['start_date'] + 
                " - " + res.json()[1]['end_date']+ "\n" + "Total: " + "$3.00")

                controller.frames[RenterReservationPage].time_slot1.set(res.json()[0]['start_date'] + 
                " - " + res.json()[0]['end_date'])
                controller.frames[RenterReservationPage].time_slot2.set(res.json()[1]['start_date'] + 
                " - " + res.json()[1]['end_date'])

                controller.frames[RenterReservationPage].parking_spot_id1.set(res.json()[0]['parking_spot_id'])
                controller.frames[RenterReservationPage].parking_spot_id2.set(res.json()[1]['parking_spot_id'])

                controller.show_frame(RenterReservationPage)

                if res.json()[0]['parking_spot']['image']  != None:
                    raw_data1 = urlopen(baseURL + res.json()[0]['parking_spot']['image']).read()
                    im1 = Image.open(BytesIO(raw_data1))
                    im1 = im1.resize((200, 150), Image.ANTIALIAS)
                    photo1 = ImageTk.PhotoImage(im1)
                    controller.frames[RenterReservationPage].garage1.config(image=photo1)
                    controller.frames[RenterReservationPage].garage1.image = photo1
                if res.json()[1]['parking_spot']['image'] != None:
                    raw_data2 = urlopen(baseURL + res.json()[1]['parking_spot']['image']).read()
                    im2 = Image.open(BytesIO(raw_data2))
                    im2 = im2.resize((200, 150), Image.ANTIALIAS)
                    photo2 = ImageTk.PhotoImage(im2)
                    controller.frames[RenterReservationPage].garage2.config(image=photo2)
                    controller.frames[RenterReservationPage].garage2.image = photo2
            

            controller.show_frame(RenterReservationPage)


        Button(self, text="Search For Parking", font=TextFont, bg="white", command=lambda: controller.show_frame(SearchPage)).pack(pady=20)
        Button(self, text="View Reservation", font=TextFont, bg="white", command=loadReservation).pack(pady=20)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).pack(pady=20)


# Client Page
class ClientPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Client Page", font=TitleFont)
        label.pack(pady=20)

        def loadClientParkingSpot():

            res = session.get(baseURL + '/parking/?client=yes')
            rate = session.get(baseURL + '/parking/admin/')

            if (len(res.json()) == 1):
                controller.frames[ParkingSpotPage].location1.config(
                    text="Location: " + res.json()[0]['street_address'] + ", " + res.json()[0]['city'] + ", " +
                         res.json()[0]['state'] + " " + res.json()[0]['zip_code']
                         + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0][
                             'end_date'] + "\nHourly Rate: $" + rate.json()['hourly_rate'])

                if res.json()[0]['image'] != None:
                    raw_data = urlopen(baseURL + res.json()[0]['image']).read()
                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((200, 150), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(im)
                    controller.frames[ParkingSpotPage].garage1.config(image=photo)
                    controller.frames[ParkingSpotPage].garage1.image = photo

            elif len(res.json()) == 2:
                controller.frames[ParkingSpotPage].location1.config(
                    text="Location: " + res.json()[0]['street_address'] + ", " + res.json()[0]['city'] + ", " +
                         res.json()[0]['state'] + " " + res.json()[0]['zip_code']
                         + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0][
                             'end_date'] + "\nHourly Rate: $" + rate.json()['hourly_rate'])
                controller.frames[ParkingDisplayPage].location2.config(
                    text="Location: " + res.json()[1]['street_address'] + ", " + res.json()[1]['city'] + ", " +
                         res.json()[1]['state'] + " " + res.json()[1]['zip_code']
                         + "\n" + "Time: " + res.json()[1]['start_date'] + "-" + res.json()[1][
                             'end_date'] + "\nHourly Rate: $" + rate.json()['hourly_rate'])
                controller.show_frame(ParkingSpotPage)

                if res.json()[0]['image'] != None:
                    raw_data1 = urlopen(baseURL + res.json()[0]['image']).read()
                    im1 = Image.open(BytesIO(raw_data1))
                    im1 = im1.resize((200, 150), Image.ANTIALIAS)
                    photo1 = ImageTk.PhotoImage(im1)
                    controller.frames[ParkingSpotPage].garage1.config(image=photo1)
                    controller.frames[ParkingSpotPage].garage1.image = photo1
                if res.json()[1]['image'] != None:
                    raw_data2 = urlopen(baseURL + res.json()[1]['image']).read()
                    im2 = Image.open(BytesIO(raw_data2))
                    im2 = im2.resize((200, 150), Image.ANTIALIAS)
                    photo2 = ImageTk.PhotoImage(im2)
                    controller.frames[ParkingSpotPage].garage2.config(image=photo2)
                    controller.frames[ParkingSpotPage].garage2.image = photo2

            controller.show_frame(ParkingSpotPage)

        Button(self, text="Add Parking Spot", font=TextFont, bg="white",
               command=lambda: controller.show_frame(AddParkingPage)).pack(pady=20)
        Button(self, text="View Parking Spot", font=TextFont, bg="white", command=loadClientParkingSpot).pack(pady=20)
        Button(self, text="View Reservation", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientReservationPage)).pack(pady=20)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(UserPage)).pack(
            pady=20)


# Renter - Reservation page
class RenterReservationPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Reservation", font=TitleFont)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        def deleteReservation(num):
            res = session.get(baseURL + '/parking/deletereserve/') # Retriveing csrftoken 
            csrftoken = res.cookies['csrftoken']
            # using csrftoken in POST request            
            
            if(num == 1 and self.parking_spot_id1.get() > 0 ):
                data = {'csrfmiddlewaretoken': csrftoken, 'deleter' : 'renter', 'time_slot' : self.time_slot1.get(), 'parking_spot_id': self.parking_spot_id1.get() }
                res = session.post(baseURL + '/parking/deletereserve/', data=data)
                print(res.json())
                if(res.json() == "Reservation Deleted"):
                    print("deleted reservation")
                    messagebox.showinfo(title="Success!", message="Reservation Deleted")
                    controller.show_frame(RenterPage)
                else:
                    messagebox.showerror('Error', 'Something Went Wrong in the backend')
            
            elif(num == 2 and self.parking_spot_id2.get() > 0):
                data = {'csrfmiddlewaretoken': csrftoken, 'deleter' : 'renter', 'time_slot' : self.time_slot2.get(), 'parking_spot_id': self.parking_spot_id2.get()}
                res = session.post(baseURL + '/parking/deletereserve/', data=data)
                print(res.json())
                if(res.json() == "Reservation Deleted"):
                    print("deleted reservation")
                    messagebox.showinfo(title="Success!", message="Reservation Deleted")
                    controller.show_frame(RenterPage)
                else:
                    messagebox.showerror('Error', 'Something Went Wrong in the backend')
            else:
                messagebox.showerror('Error', 'No Reservation')
                

        self.time_slot1 = StringVar()
        self.time_slot2 = StringVar()

        self.parking_spot_id1 = IntVar()
        self.parking_spot_id2 = IntVar()



        garage1 = Image.open("no_image.png").resize((200, 150))
        garage_img1 = ImageTk.PhotoImage(garage1)

        garage2 = Image.open("no_image.png").resize((200, 150))
        garage_img2 = ImageTk.PhotoImage(garage2)

        clientname1 = "N/A"
        address1 = "N/A"
        timeseleted1 = "N/A"
        total1 = "$0.00"

        clientname2 = "N/A"
        address2 = "N/A"
        timeseleted2 = "N/A"
        total2 = "$0.00"

        self.garage1 = Label(self, image=garage_img1)
        self.garage1.image = garage_img1
        self.garage1.grid(row=1, column=0, pady=15)
        
        self.resv_label1 = Label(self, font=TextFont, text="Owner of Parking Spot: " + clientname1 + "\n" + "Location: " + address1 + "\n" + "Time Slot: " + timeseleted1 + "\n" + "Total: " + total1)
        self.resv_label1.grid(row=2, column=0)
        Button(self, text="cancel", font=TextFont, bg="white", command=lambda: deleteReservation(1)).grid(row=2, column=1, pady=15, padx=10)

        self.garage2 = Label(self, image=garage_img2)
        self.garage2.image = garage_img2
        self.garage2.grid(row=3, column=0, pady=15)
        self.resv_label2 = Label(self, font=TextFont, text="Owner of Parking Spot: " + clientname2 + "\n" + "Location: " + address2 + "\n" + "Time Slot: " + timeseleted2 + "\n" + "Total: " + total2)
        self.resv_label2.grid(row=4, column=0)
        Button(self, text="cancel", font=TextFont, bg="white", command=lambda: deleteReservation(2)).grid(row=4, column=1, pady=15, padx=10)

        Button(self, text="back", font=TextFont, bg="white", command=lambda: controller.show_frame(RenterPage)).grid(row=5, column=0, pady=15, columnspan=2)


# Renter Search Page
class SearchPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Find Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=15)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        start_clicked = StringVar()
        start_clicked.set(time_option[0])

        end_clicked = StringVar()
        end_clicked.set(time_option[0])

        # Date & Time
        Label(self, text="Day & Time:*", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, start_clicked, *time_option)
        start_time.grid(row=1, column=2)

        
        # Location
        Label(self, text="Street:", font=TextFont).grid(row=3, column=0, pady=15, sticky="e")
        street_entry = Entry(self, font=TextFont)
        street_entry.grid(row=3, column=1)

        Label(self, text="City:", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=4, column=1)

        Label(self, text="State:", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=5, column=1)

        Label(self, text="Zip Code:*", font=TextFont).grid(row=6, column=0, pady=15, sticky="e")
        zipcode_entry = Entry(self, font=TextFont)
        zipcode_entry.grid(row=6, column=1)


        def loadSearchPage():
            res = session.get(baseURL + '/parking/?date='+str(start_cal.get_date())+':'+ start_clicked.get())
            if not zipcode_entry.get() or not start_cal.get():
                messagebox.showerror('Error', 'Please fill in all * area')
            else:
                res = session.get(baseURL + '/parking/?date='+str(start_cal.get_date())+':'+ start_clicked.get())
                rate = session.get(baseURL + '/parking/admin/')
                if len(res.json()) == 1:
                    controller.frames[ParkingDisplayPage].location1.config(text="Location: " + res.json()[0]['street_address']+", " + res.json()[0]['city']+", " + res.json()[0]['state'] + " " + res.json()[0]['zip_code']
                    + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0]['end_date'] + "\nHourly Rate: $" + rate.json()['hourly_rate'])

                    controller.frames[ParkingDisplayPage].spot_id1.set(res.json()[0]['id'])
                    controller.frames[ParkingDisplayPage].client_id1.set(res.json()[0]['client_id'])
                    
                    if(res.json()[0]['image'] != None):
                        raw_data = urlopen(baseURL + res.json()[0]['image'] ).read()
                        im = Image.open(BytesIO(raw_data))
                        im = im.resize((200, 150), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(im)
                        controller.frames[ParkingDisplayPage].garage1.config(image=photo)
                        controller.frames[ParkingDisplayPage].garage1.image = photo

                    controller.show_frame(ParkingDisplayPage)
                
                elif( len(res.json()) == 2):
                    controller.frames[ParkingDisplayPage].location1.config(text="Location: " + res.json()[0]['street_address']+", " + res.json()[0]['city']+", " + res.json()[0]['state'] + " " + res.json()[0]['zip_code'] 
                    + "\n" + "Time: " + res.json()[0]['start_date'] + "-" + res.json()[0]['end_date'] + "\nHourly Rate: $$" + rate.json()['hourly_rate'])
                    controller.frames[ParkingDisplayPage].location2.config(text="Location: " + res.json()[1]['street_address']+", " + res.json()[1]['city']+", " + res.json()[1]['state'] + " " + res.json()[1]['zip_code'] 
                    + "\n" + "Time: " + res.json()[1]['start_date'] + "-" + res.json()[1]['end_date'] + "\nHourly Rate: $$" + rate.json()['hourly_rate'])
                    controller.show_frame(ParkingDisplayPage)

                    controller.frames[ParkingDisplayPage].spot_id1.set(res.json()[0]['id'])
                    controller.frames[ParkingDisplayPage].client_id1.set(res.json()[0]['client_id'])
                    controller.frames[ParkingDisplayPage].spot_id2.set(res.json()[1]['id'])
                    controller.frames[ParkingDisplayPage].client_id2.set(res.json()[1]['client_id'])

                    if(res.json()[0]['image'] != None):
                        raw_data1 = urlopen(baseURL + res.json()[0]['image'] ).read()
                        im1 = Image.open(BytesIO(raw_data1))
                        im1 = im1.resize((200, 150), Image.ANTIALIAS)
                        photo1 = ImageTk.PhotoImage(im1)
                        controller.frames[ParkingDisplayPage].garage1.config(image=photo1)
                        controller.frames[ParkingDisplayPage].garage1.image = photo1
                    if res.json()[1]['image'] != None:
                        raw_data2 = urlopen(baseURL + res.json()[1]['image']).read()
                        im2 = Image.open(BytesIO(raw_data2))
                        im2 = im2.resize((200, 150), Image.ANTIALIAS)
                        photo2 = ImageTk.PhotoImage(im2)
                        controller.frames[ParkingDisplayPage].garage2.config(image=photo2)
                        controller.frames[ParkingDisplayPage].garage2.image = photo2
                    
                else:
                    messagebox.showerror("No Parking Spot Found", message="Change search parameters and try again")

        Button(self, text="Search", font=TextFont, bg="white", command=loadSearchPage).grid(row=9, column=2, pady=15, sticky="e")
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(RenterPage)).grid(row=9, column=0, pady=15, sticky="w")


# Renter - Display Parking
class ParkingDisplayPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Available Parking", font=TitleFont)
        label.grid(row=0, column=0, columnspan= 2, pady=15)

        def reserve(spotNum):
            
            if(spotNum == 1):
                spot_id = self.spot_id1.get()
                client_id = self.client_id1.get()
                start_time = self.start_clicked1.get()
                end_time = self.end_clicked1.get()
                
            else:
                spot_id = self.spot_id2.get()
                client_id = self.client_id2.get()
                start_time = self.start_clicked2.get()
                end_time = self.end_clicked2.get()

                
            res = session.get(baseURL + '/parking/reserve/') # Retriveing csrftoken 
            csrftoken = res.cookies['csrftoken']
            # using csrftoken in POST request
            data = {'csrfmiddlewaretoken': csrftoken, 'client_id' : client_id, 'parking_spot_id' : spot_id, 'start_time' : start_time, 'end_time' : end_time }
            res = session.post(baseURL + '/parking/reserve/', data=data)

            if(res.json() == "Reservation Created"):
                messagebox.showinfo(title="Success", message="Your parking spot is successfully reserved.")
                controller.show_frame(UserPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")
               

        address1 = "N/A"
        address2 = "N/A"

        availabletime1 = "N/A"
        availabletime2 = "N/A"
        
        hourly_rate = "N/A"

        garage1 = Image.open("no_image.png").resize((200, 150))
        garage1_img = ImageTk.PhotoImage(garage1)

        garage2 = Image.open("no_image.png").resize((200, 150))
        garage2_img = ImageTk.PhotoImage(garage2)
        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        self.start_clicked1 = StringVar()
        self.start_clicked1.set(time_option[0])
        self.end_clicked1 = StringVar()
        self.end_clicked1.set(time_option[0])


        self.start_clicked2 = StringVar()
        self.start_clicked2.set(time_option[0])
        self.end_clicked2 = StringVar()
        self.end_clicked2.set(time_option[0])

        self.spot_id1 = IntVar() # This id is used for identifying parking spot #1 in the database
        self.spot_id2 = IntVar() # This id is used for identifying parking spot #2 in the database
        self.client_id1 = IntVar() # This id is used for identifying the owner of spot #1 in the database
        self.client_id2 = IntVar()# This id is used for identifying the owner of spot #2 in the database
        
        
        # Parking Garage 1
        self.garage1 = Label(self, image=garage1_img)
        self.garage1.image = garage1_img
        self.garage1.grid(row=1, column=0, pady=15)
        start_time1 = OptionMenu(self, self.start_clicked1, *time_option)
        start_time1.grid(row=1, column=1)
        Label(self, text="   to   ").grid(row=1, column=2)
        end_time1 = OptionMenu(self, self.end_clicked1, *time_option)
        end_time1.grid(row=1, column=3)
        self.location1 = Label(self, text="Location: " + address1 + "\n" + "Time: " + availabletime1 + "\n" + "Hourly Rate: " + hourly_rate)
        self.location1.grid(row=2, column=0, sticky="w")
        reserve1 = Button(self, text="Reserve", command=lambda: reserve(1))
        reserve1.grid(row=2, column=1, pady=15, columnspan=3)

        # Parking Garage 2
        self.garage2 = Label(self, image=garage2_img)
        self.garage2.image = garage2_img
        self.garage2.grid(row=3, column=0, pady=15)
        start_time1 = OptionMenu(self, self.start_clicked2, *time_option)
        start_time1.grid(row=3, column=1)
        Label(self, text="   to   ").grid(row=3, column=2)
        end_time1 = OptionMenu(self, self.end_clicked2, *time_option)
        end_time1.grid(row=3, column=3)
        self.location2 = Label(self, text="Location: " + address2 + "\n" + "Time: " + availabletime2 + "\n" + "Hours Rate: " + hourly_rate)
        self.location2.grid(row=4, column=0, sticky="w")
        reserve2 = Button(self, text="Reserve", command=lambda: reserve(2))
        reserve2.grid(row=4, column=1, pady=15, columnspan=3)

        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(SearchPage)).grid(row=5, column=0, pady=15, columnspan=3)


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

        self.filename = StringVar()

        def added():
            if not zipcode_entry.get() or not state_entry.get() or not city_entry.get() or not street_entry.get() or not start_cal.get() or not end_cal.get():
                messagebox.showerror('Error', 'Please fill in all * area')
            else:
                # When doing post requests we need to retrieve the csrftoken with a GET request then we can do a POST request
                res = session.get(baseURL + "/parking/")  # Retriveing csrftoken
                csrftoken = res.cookies['csrftoken']
                # using csrftoken in POST request
                data = {'csrfmiddlewaretoken': csrftoken, 'street_address': street_entry.get().lower(),
                        'city': city_entry.get().lower(), 'state': state_entry.get().lower(),
                        'zip_code': zipcode_entry.get(), 
                        'start_date': start_cal.get_date(), 'start_time': clicked_start.get(),
                        'end_date': end_cal.get_date(), 'end_time': clicked_end.get()}
                files = {'media': open(self.filename.get(), 'rb')}
                res = session.post(url=(baseURL + "/parking/"), data=data, files=files)
            if res.json() == "New Spot Created":
                messagebox.showinfo(title="Success", message="Successfully Added Parking Sot")
                controller.show_frame(ClientPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")

        def save_png():
            try:
                global img
                filetypes = [("PNG", "*.png"), ("JPG", "*.jpg")]
                self.filepath = filedialog.askopenfilename(title='Open files', initialdir='C:/Users/Administrator/Desktop', filetypes=filetypes, defaultextension='.jpg')
                self.filename.set(self.filepath)
                img = Image.open(self.filename.get())
            except Exception as e:
                print(e)


        # Start Date & Time
        Label(self, text="Start Day & Time:*", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked_start, *time_option)
        start_time.grid(row=1, column=2)

        # End Date & Time
        Label(self, text="End Day & Time:*", font=TextFont).grid(row=2, column=0, pady=15, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked_end, *time_option)
        end_time.grid(row=2, column=2)

        # Location - Street, City, State, Zipcode
        Label(self, text="Street:", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        street_entry = Entry(self, font=TextFont)
        street_entry.grid(row=4, column=1)
        Label(self, text="City:", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=5, column=1)
        Label(self, text="State:", font=TextFont).grid(row=6, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=6, column=1)
        Label(self, text="Zip Code:*", font=TextFont).grid(row=7, column=0, pady=15, sticky="e")
        zipcode_entry = Entry(self, font=TextFont)
        zipcode_entry.grid(row=7, column=1)


        # Upload image
        Label(self, text="Image: ", font=TextFont).grid(row=10, column=0, pady=15, sticky="e")
        # Button(self, text="image path", command=open_img).grid(row=7, column=1, pady=15)
        Button(self, text="upload", font=TextFont, command=save_png, bg="white").grid(row=10, column=1, pady=15)

        Button(self, text="Add", font=TextFont, bg="white", command=added).grid(row=11, column=2, pady=15)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage)).grid(row=11, column=0, pady=15, sticky="e")


# Client - Parking Spot
class ParkingSpotPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="My Parking Spots", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, pady=15)

        def delete(spotNum):
            messagebox.showinfo(title="Success", message="Parking Spot Deleted")

            controller.show_frame(ParkingSpotPage)
        
        def modify(spotNum):
            messagebox.showinfo(title="Success", message="Parking Spot Modified")

            controller.show_frame(ModifySpotPage)

        address1 = "N/A"
        address2 = "N/A"

        availabletime1 = "N/A"
        availabletime2 = "N/A"
        
        hourly_rate = "N/A"

        garage1 = Image.open("no_image.png").resize((200, 150))
        garage1_img = ImageTk.PhotoImage(garage1)

        garage2 = Image.open("no_image.png").resize((200, 150))
        garage2_img = ImageTk.PhotoImage(garage2)

        # Parking Garage 1
        self.garage1 = Label(self, image=garage1_img)
        self.garage1.image = garage1_img
        self.garage1.grid(row=1, column=0, pady=15)
        self.location1 = Label(self, text="Location: " + address1 + "\n" + "Time: " + availabletime1 + "\n" + "Hourly Rate: " + hourly_rate)
        self.location1.grid(row=2, column=0, sticky="w")

        modify1 = Button(self, text="Modify", command=lambda: modify(1), bg="white", font=TextFont)
        modify1.grid(row=2, column=1)
        delete1 = Button(self, text="Delete", command=lambda: delete(1), bg="white", font=TextFont)
        delete1.grid(row=2, column=2)

        # Parking Garage 2
        self.garage2 = Label(self, image=garage2_img)
        self.garage2.image = garage2_img
        self.garage2.grid(row=3, column=0, pady=15)
        self.location2 = Label(self, text="Location: " + address2 + "\n" + "Time: " + availabletime2 + "\n" + "Hours Rate: " + hourly_rate)
        self.location2.grid(row=4, column=0)
        
        modify2 = Button(self, text="Modify", command=lambda: modify(2), bg="white", font=TextFont)
        modify2.grid(row=4, column=1)
        delete2 = Button(self, text="Delete", command=lambda: delete(2), bg="white", font=TextFont)
        delete2.grid(row=4, column=2)

        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage)).grid(row=5, column=0, pady=15, columnspan=3)


# Client - Modify Parking Spot
class ModifySpotPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Modify Parking Spot", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        time_option = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
                       "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                       "20:00", "21:00", "22:00", "23:00"]

        clicked_start = StringVar()
        clicked_start.set(time_option[0])

        clicked_end = StringVar()
        clicked_end.set(time_option[0])

        self.filename = StringVar()

        def added():
            # When doing post requests we need to retrieve the csrftoken with a GET request then we can do a POST request

            res = session.get(baseURL + "/parking/")  # Retriveing csrftoken
            csrftoken = res.cookies['csrftoken']
            # using csrftoken in POST request
            data = {'csrfmiddlewaretoken': csrftoken, 'street_address': street_entry.get().lower(),
                    'city': city_entry.get().lower(), 'state': state_entry.get().lower(),
                    'zip_code': zipcode_entry.get(),
                    'start_date': start_cal.get_date(), 'start_time': clicked_start.get(),
                    'end_date': end_cal.get_date(), 'end_time': clicked_end.get()}

            files = {'media': open(self.filename.get(), 'rb')}

            res = session.post(url=(baseURL + "/parking/"), data=data, files=files)
            if res.json() == "New Spot Created":
                messagebox.showinfo(title="Success", message="Successfully Added Parking Sot")
                controller.show_frame(ClientPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")

        def save_png():
            try:
                global img
                filetypes = [("PNG", "*.png"), ("JPG", "*.jpg")]
                self.filepath = filedialog.askopenfilename(title='Open files',
                                                           initialdir='C:/Users/Administrator/Desktop',
                                                           filetypes=filetypes, defaultextension='.jpg')
                self.filename.set(self.filepath)
                img = Image.open(self.filename.get())
            except Exception as e:
                print(e)

        # Start Date & Time
        Label(self, text="Start Day & Time:*", font=TextFont).grid(row=1, column=0, pady=15, sticky="e")
        start_cal = DateEntry(self, selectmode='day')
        start_cal.grid(row=1, column=1)
        start_time = OptionMenu(self, clicked_start, *time_option)
        start_time.grid(row=1, column=2)

        # End Date & Time
        Label(self, text="End Day & Time:*", font=TextFont).grid(row=2, column=0, pady=15, sticky="e")
        end_cal = DateEntry(self, selectmode='day')
        end_cal.grid(row=2, column=1)
        end_time = OptionMenu(self, clicked_end, *time_option)
        end_time.grid(row=2, column=2)

        # Location - Street, City, State, Zipcode
        Label(self, text="Street:*", font=TextFont).grid(row=4, column=0, pady=15, sticky="e")
        street_entry = Entry(self, font=TextFont)
        street_entry.grid(row=4, column=1)
        Label(self, text="City:* ", font=TextFont).grid(row=5, column=0, pady=15, sticky="e")
        city_entry = Entry(self, font=TextFont)
        city_entry.grid(row=5, column=1)
        Label(self, text="State:*", font=TextFont).grid(row=6, column=0, pady=15, sticky="e")
        state_entry = Entry(self, font=TextFont)
        state_entry.grid(row=6, column=1)
        Label(self, text="Zip Code:*", font=TextFont).grid(row=7, column=0, pady=15, sticky="e")
        zipcode_entry = Entry(self, font=TextFont)
        zipcode_entry.grid(row=7, column=1)

        # Upload image
        Label(self, text="Image: ", font=TextFont).grid(row=10, column=0, pady=15, sticky="e")
        # Button(self, text="image path", command=open_img).grid(row=7, column=1, pady=15)
        Button(self, text="upload", font=TextFont, command=save_png, bg="white").grid(row=10, column=1, pady=15)

        Button(self, text="Save", font=TextFont, bg="white", command=added).grid(row=11, column=2, pady=15)
        Button(self, text="Back", font=TextFont, bg="white", command=lambda: controller.show_frame(ParkingSpotPage)).grid(
            row=11, column=0, pady=15, sticky="e")


# Client - Reservation page
class ClientReservationPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Reservation", font=TitleFont)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        garage1 = Image.open("no_image.png").resize((200, 150))
        garage_img1 = ImageTk.PhotoImage(garage1)

        garage2 = Image.open("no_image.png").resize((200, 150))
        garage_img2 = ImageTk.PhotoImage(garage2)

        rentername1 = "N/A"
        address1 = "N/A"
        timeseleted1 = "N/A"
        totalhrs1 = "0"

        rentername2 = "N/A"
        address2 = "N/A"
        timeseleted2 = "N/A"
        totalhrs2 = "0"

        self.garage1 = Label(self, image=garage_img1)
        self.garage1.image = garage_img1
        self.garage1.grid(row=1, column=0, pady=15)
        resv_label = Label(self, font=TextFont, text="Renter: " + rentername1 + "\n" + "Location: " + address1 + "\n" + "Time: " + timeseleted1 + "\n" + "Total hours: " + totalhrs1)
        resv_label.grid(row=2, column=0)
        Button(self, text="cancel", font=TextFont, bg="white").grid(row=2, column=1, pady=15, padx=10)

        self.garage2 = Label(self, image=garage_img2)
        self.garage2.image = garage_img2
        self.garage2.grid(row=3, column=0, pady=15)
        resv_label = Label(self, font=TextFont, text="Renter: " + rentername2 + "\n" + "Location: " + address2 + "\n" + "Time: " + timeseleted2 + "\n" + "Total hours: " + totalhrs2)
        resv_label.grid(row=4, column=0)
        Button(self, text="cancel", font=TextFont, bg="white").grid(row=4, column=1, pady=15, padx=10)

        Button(self, text="back", font=TextFont, bg="white", command=lambda: controller.show_frame(ClientPage)).grid(row=5, column=0, pady=15, columnspan=2)


# Account Page
class AccountPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Account", font=TitleFont)
        label.pack(pady=20)


        def view_account():

            user_info = session.get(baseURL + '/users/').json()
            user_bank_info = session.get(baseURL + '/payment/').json()
            
            controller.frames[ViewAcctPage].fn_display.config(text="First Name: " + user_info['first_name'])
            controller.frames[ViewAcctPage].ln_display.config(text="Last Name: " + user_info['last_name'])
            controller.frames[ViewAcctPage].email_display.config(text="Email Address: " + user_info['email'])
            controller.frames[ViewAcctPage].phone_display.config(text="Phone#: " + user_info['phoneNum'])

            controller.frames[ViewAcctPage].bank_display.config(text="Bank Name: " + user_bank_info['bank_name'])
            controller.frames[ViewAcctPage].routing_display.config(text="Routing Number: " + user_bank_info['routing_number'])
            controller.frames[ViewAcctPage].account_display.config(text="Account Number: " + user_bank_info['account_number'])

            controller.show_frame(ViewAcctPage)


        #  View Account
        view_button = Button(self, text="View Account", font=TextFont, bg="white", command=view_account)
        view_button.pack(pady=20)
        # Update Account
        edit_button = Button(self, text="Update Account", font=TextFont, bg="white", command=lambda: controller.show_frame(AcctUpdatePage))
        edit_button.pack(pady=20)
        # Delete Account
        delete_button = Button(self, text="Delete Account", font=TextFont, bg="white", command=lambda: controller.show_frame(AcctDeletePage))
        delete_button.pack(pady=20)
        
        Button(self, text="Back", command=lambda: controller.show_frame(UserPage), font=TextFont, bg="white").pack(pady=20)
                

# View Account Page
class ViewAcctPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="View", font=TitleFont)
        label.pack(pady=10)

        fn_display = "N/A"
        ln_display = "N/A"
        email_display = "N/A"
        phone_display = "N/A"
        bank_display = "N/A"
        routing_display = "N/A"
        account_display = "N/A"

        # First Name
        self.fn_display = Label(self, text="First Name: " + fn_display, font=TextFont)
        self.fn_display.pack(pady=10)

        # Last Name
        self.ln_display = Label(self, text="Last Name: " + ln_display, font=TextFont)
        self.ln_display.pack(pady=10)

        # Email
        self.email_display = Label(self, text="Email Address: " + email_display, font=TextFont)
        self.email_display.pack(pady=10)

        # Phone Number
        self.phone_display = Label(self, text="Phone#: " + phone_display, font=TextFont)
        self.phone_display.pack(pady=10)

        # Bank Info
        self.bank_display = Label(self, text="Bank Name: " + bank_display, font=TextFont)
        self.bank_display.pack(pady=10)

        # Routing Number
        self.routing_display = Label(self, text="Routing Number: " + routing_display, font=TextFont)
        self.routing_display.pack(pady=10)

        # Account Number
        self.account_display = Label(self, text="Account Number: " + account_display, font=TextFont)
        self.account_display.pack(pady=10)
        
        Button(self, text="Back", command=lambda:controller.show_frame(AccountPage), font=TextFont).pack(pady=10)

# Update Account page
class AcctUpdatePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Update", font=TitleFont)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        Label(self, text="*Please fill in what you would like to update:", font=("Times", 15)).grid(row=1, column=0, columnspan=2, pady=5, sticky="nw")

        def update():

            res = session.get(baseURL + "/users/update/")  # Retrieving csrftoken
            csrftoken = res.cookies['csrftoken']

            res = session.post(baseURL + '/users/update/', data={'csrfmiddlewaretoken': csrftoken, 'first_name': fn_entry.get(), 'last_name': ln_entry.get(),
            'email': email_entry.get(), 'phone': phone_entry.get(), 'bank_name': bank_entry.get(), 'routing': routing_entry.get(),
            'account': account_entry.get()
             })

            if res.json() == "User Updated":
                messagebox.showinfo(title="Success", message="Account has been!")
                newRes = session.get(baseURL + '/users/')  # GET Request to retrieve user info after update
                controller.frames[UserPage].label.config(text="Welcome " + newRes.json()['first_name'] + "!")  # Update the Welcome Label in UserPage with the user's name
                #### Make other updates to user's account 
                ###
                ###
                ###
                controller.show_frame(UserPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")

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
        pw_entry = Entry(self, font=TextFont)
        pw_entry.grid(row=6, column=1, sticky="w")

        # Bank Info
        Label(self, text="Bank Name:", font=TextFont).grid(row=8, column=0, pady=5, sticky="e")
        bank_entry = Entry(self, font=TextFont)
        bank_entry.grid(row=8, column=1, sticky="w")

        # Routing Number
        Label(self, text="Routing Number:", font=TextFont).grid(row=9, column=0, sticky="e")
        routing_entry = Entry(self, font=TextFont)
        routing_entry.grid(row=9, column=1, sticky="w")

        # Account Number
        Label(self, text="Account Number:", font=TextFont).grid(row=10, column=0, pady=5, sticky="e")
        account_entry = Entry(self, font=TextFont)
        account_entry.grid(row=10, column=1, sticky="w")

        Button(self, text="Back", command=lambda: controller.show_frame(AccountPage), font=TextFont, bg="white").grid(row=11, column=0)
        Button(self, text="Confirm Update", font=TextFont, bg="white", command=update).grid(row=11, column=1, padx=10, pady=10)


# Delete Account page
class AcctDeletePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Delete Account", font=TitleFont)
        label.pack(pady=20)

        def deleteAcc():
            res = session.get(baseURL + "/users/delete/") # Retriveing csrftoken 
            csrftoken = res.cookies['csrftoken']

            res = session.post(baseURL + '/users/delete/', data={'csrfmiddlewaretoken': csrftoken})
            if res.json() == "User Deleted":
                messagebox.showinfo(title="Deleted", message="User Account Is Deleted")
                controller.show_frame(LoginPage)
            else:
                messagebox.showerror("Error", message="Something went wrong with backend server!")
        
        Button(self, text="Confirm Delete", font=TextFont, bg="white", command=deleteAcc).pack(pady=20)
        Button(self, text="Back", command=lambda: controller.show_frame(AccountPage), font=TextFont, bg="white").pack(pady=20)


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
                if pw_entry.get() != confirm_entry.get():
                    messagebox.showerror('Error', message='Password and confirm password must be the same!')
                    if type(phone_entry.get()) != int and len(phone_entry.get()) != 10:
                        messagebox.showerror('Error', message='Phone Number enter is increase!')
                        if not email_entry.get():
                            messagebox.showerror('Error', message='Email enter is increase!')
            else:
                
                data = {'first_name': fn_entry.get(), 'last_name': ln_entry.get(), 'email': email_entry.get(), 'password': pw_entry.get(),
                'phone': phone_entry.get(), 'bank_name': bank_entry.get(), 'routing': routing_entry.get(), 'account': account_entry.get()}
                res = session.post(baseURL + '/users/signup/', data)
                
                if res.json() == "New User Created":
                    messagebox.showinfo(title="Success", message="Successfully Signed Up")
                    controller.show_frame(LoginPage) 
                else:
                    messagebox.showerror('Error', message='Something went wrong in the backend')

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

        Button(self, text="Confirm", command=verifyAcc, font=TextFont, bg="white").grid(row=13, column=1, pady=30, sticky="e")
        Button(self, text="Back", command=lambda: controller.show_frame(LoginPage), font=TextFont, bg="white").grid(row=13, column=0)


# Driver Code
app = EasyPark()
app.mainloop()
