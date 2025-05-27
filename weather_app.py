from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from tkinter import messagebox
from timezonefinder import TimezoneFinder

root = Tk()
root.title("Weather App")
root.geometry("750x520+300+100")
root.resizable(False, False)
root.config(bg="#202731")

# Weather Function
def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N {round(location.longitude, 4)}°E")
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    api_key = "7abc43361506f39a7a308edc5d72766c"
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    json_data = requests.get(api).json()

    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed = current['wind']['speed']
    description = current['weather'][0]['description']

    t.config(text=f"{round(temp - 273.15, 2)}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description.capitalize()}")

    daily_data = []
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)

    icons = []
    temps = []

    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        img = Image.open(f"icon/{icon_code}@2x.png").resize((50, 50))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like']))

    day_widget = [
        (firstimage, day1, day1temp),
        (secondimage, day2, day2temp),
        (thirdimage, day3, day3temp),
        (fourthimage, day4, day4temp),
        (fifthimage, day5, day5temp)
    ]

    for i, (img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day: {round(temps[i][0] - 273.15, 1)}°C\nFeels: {round(temps[i][1] - 273.15, 1)}°C")
        future_day = datetime.now() + timedelta(days=i)
        day_label.config(text=future_day.strftime("%A"))

# UI Elements
image_icon = PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

Round_box = PhotoImage(file="Images/Rounded Rectangle 1.png")
Label(root, image=Round_box, bg="#202731").place(x=30, y=60)

Label(root, text="Temperature", font=("Helvetica", 11), fg="#323661", bg="#aad1c8").place(x=50, y=120)
Label(root, text="Humidity", font=("Helvetica", 11), fg="#323661", bg="#aad1c8").place(x=50, y=140)
Label(root, text="Pressure", font=("Helvetica", 11), fg="#323661", bg="#aad1c8").place(x=50, y=160)
Label(root, text="Wind Speed", font=("Helvetica", 11), fg="#323661", bg="#aad1c8").place(x=50, y=180)
Label(root, text="Description", font=("Helvetica", 11), fg="#323661", bg="#aad1c8").place(x=50, y=200)

Search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
Label(root, image=Search_image, bg="#202731").place(x=270, y=122)

weat_image = PhotoImage(file="Images/Layer 7.png")
Label(root, image=weat_image, bg="#333c4c").place(x=290, y=127)

textfield = tk.Entry(root, justify="center", width=15, font=("poppins", 25, "bold"), bg="#333c4c", border=0, fg="white")
textfield.place(x=370, y=130)

Search_icon = PhotoImage(file="Images/Layer 6.png")
Button(root, image=Search_icon, borderwidth=0, cursor="hand2", bg="#333c4c", command=getWeather).place(x=640, y=135)

clock = Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
clock.place(x=30, y=20)

timezone = Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
timezone.place(x=500, y=20)

long_lat = Label(root, font=("Helvetica", 10), bg="#202731", fg="white")
long_lat.place(x=500, y=50)

t = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
t.place(x=150, y=120)

h = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
h.place(x=150, y=140)

p = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
p.place(x=150, y=160)

w = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
w.place(x=150, y=180)

d = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
d.place(x=150, y=200)

# Forecast boxes
firstframe = Frame(root, width=120, height=120, bg="#323661")
firstframe.place(x=30, y=380)
firstimage = Label(firstframe, bg="#323661")
firstimage.pack()
day1 = Label(firstframe, font=("arial", 10), bg="#323661", fg="white")
day1.pack()
day1temp = Label(firstframe, font=("arial", 10), bg="#323661", fg="white")
day1temp.pack()

secondframe = Frame(root, width=120, height=120, bg="#323661")
secondframe.place(x=160, y=380)
secondimage = Label(secondframe, bg="#323661")
secondimage.pack()
day2 = Label(secondframe, font=("arial", 10), bg="#323661", fg="white")
day2.pack()
day2temp = Label(secondframe, font=("arial", 10), bg="#323661", fg="white")
day2temp.pack()

thirdframe = Frame(root, width=120, height=120, bg="#323661")
thirdframe.place(x=290, y=380)
thirdimage = Label(thirdframe, bg="#323661")
thirdimage.pack()
day3 = Label(thirdframe, font=("arial", 10), bg="#323661", fg="white")
day3.pack()
day3temp = Label(thirdframe, font=("arial", 10), bg="#323661", fg="white")
day3temp.pack()

fourthframe = Frame(root, width=120, height=120, bg="#323661")
fourthframe.place(x=420, y=380)
fourthimage = Label(fourthframe, bg="#323661")
fourthimage.pack()
day4 = Label(fourthframe, font=("arial", 10), bg="#323661", fg="white")
day4.pack()
day4temp = Label(fourthframe, font=("arial", 10), bg="#323661", fg="white")
day4temp.pack()

fifthframe = Frame(root, width=120, height=120, bg="#323661")
fifthframe.place(x=550, y=380)
fifthimage = Label(fifthframe, bg="#323661")
fifthimage.pack()
day5 = Label(fifthframe, font=("arial", 10), bg="#323661", fg="white")
day5.pack()
day5temp = Label(fifthframe, font=("arial", 10), bg="#323661", fg="white")
day5temp.pack()

root.mainloop()