import tkinter as tk
import requests
from tkinter import Canvas
import math
import random

api_key = "30d4741c779ba94c470ca1f63045390a"

# --- Weather Fetching ---
def get_weather():
    city = city_entry.get()
    if not city or city == "Enter city name":
        weather_label.config(text="Please enter a city", fg="#E74C3C")
        clear_weather_display()
        return

    units = "metric" if metric_var.get() else "imperial"
    unit_symbol = "ºC" if metric_var.get() else "ºF"

    weather_label.config(text="")
    draw_loading()
    temp_label.config(text="")

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            raise ValueError(data.get("message", "Error"))

        weather = data["weather"][0]["main"]
        temp = round(data["main"]["temp"])

        draw_weather_icon(weather)
        weather_label.config(text=weather, fg="#34495E")
        temp_label.config(text=f"{temp}{unit_symbol}", fg="#34495E")

    except Exception as e:
        clear_weather_display()
        weather_label.config(text="Error fetching weather", fg="#E74C3C")

# --- Draw Functions ---
def draw_loading():
    canvas.delete("all")
    canvas.create_text(75, 50, text="⏳", font=("Arial", 36))

def clear_weather_display():
    canvas.delete("all")
    weather_label.config(text="")
    temp_label.config(text="")

def draw_weather_icon(condition):
    canvas.delete("all")
    if condition == "Clouds":
        animate_clouds()
    elif condition == "Clear":
        animate_sun()
    elif condition == "Rain":
        animate_rain()
    elif condition == "Snow":
        animate_snow()
    elif condition in ["Mist", "Fog", "Haze"]:
        animate_fog()
    else:
        canvas.create_text(75, 50, text="❔", font=("Arial", 40))

def animate_clouds():
    canvas.delete("all")
    cloud_parts = [
        canvas.create_oval(40, 60, 90, 100, fill="gray", outline=""),
        canvas.create_oval(60, 40, 110, 90, fill="gray", outline=""),
        canvas.create_oval(80, 60, 130, 100, fill="gray", outline=""),
        canvas.create_oval(50, 70, 120, 110, fill="gray", outline="")
    ]
    direction = [1]

    def move_clouds():
        for part in cloud_parts:
            canvas.move(part, direction[0], 0)
        x1, _, x2, _ = canvas.bbox(cloud_parts[0])
        if x2 > 150 or x1 < 0:
            direction[0] *= -1
        canvas.after(100, move_clouds)

    move_clouds()

def animate_sun():
    canvas.delete("all")

    # Sun glow (aura)
    for r, color in [(70, "#FFF9C4"), (60, "#FFF176"), (50, "yellow")]:
        canvas.create_oval(75 - r//2, 65 - r//2, 75 + r//2, 65 + r//2, fill=color, outline="")

    # Sun center
    canvas.create_oval(55, 45, 95, 85, fill="gold", outline="orange", width=2)

    # Animated rays
    rays = []
    for i in range(12):  # 12 rays instead of 8
        angle = i * math.pi / 6
        x1 = 75 + 30 * math.cos(angle)
        y1 = 65 + 30 * math.sin(angle)
        x2 = 75 + 45 * math.cos(angle)
        y2 = 65 + 45 * math.sin(angle)
        ray = canvas.create_line(x1, y1, x2, y2, fill="orange", width=2)
        rays.append(ray)

    # Ray animation (subtle pulsing)
    pulse_dir = [1]

    def pulse():
        for ray in rays:
            canvas.itemconfigure(ray, width=2 + pulse_dir[0])
        pulse_dir[0] *= -1
        canvas.after(500, pulse)

    pulse()


def animate_rain():
    canvas.delete("all")
    cloud_parts = [
        canvas.create_oval(40, 60, 90, 100, fill="gray", outline=""),
        canvas.create_oval(60, 40, 110, 90, fill="gray", outline=""),
        canvas.create_oval(80, 60, 130, 100, fill="gray", outline=""),
        canvas.create_oval(50, 70, 120, 110, fill="gray", outline="")
    ]

    drops = []
    for _ in range(20):
        x = random.randint(50, 130)
        y = random.randint(110, 180)
        length = random.randint(10, 20)
        speed = random.uniform(2, 5)
        drop = canvas.create_line(x, y, x, y + length, fill="blue", width=2)
        drops.append({"id": drop, "speed": speed, "length": length})

    def rain():
        for drop in drops:
            canvas.move(drop["id"], 0, drop["speed"])
            x1, y1, x2, y2 = canvas.coords(drop["id"])
            if y1 > 130:
                new_x = random.randint(50, 130)
                new_y = random.randint(110, 120)
                canvas.coords(drop["id"], new_x, new_y, new_x, new_y + drop["length"])
        canvas.after(50, rain)

    rain()

def animate_snow():
    cloud_parts = [
        canvas.create_oval(40, 60, 90, 100, fill="lightgray", outline=""),
        canvas.create_oval(60, 40, 110, 90, fill="lightgray", outline=""),
        canvas.create_oval(80, 60, 130, 100, fill="lightgray", outline=""),
        canvas.create_oval(50, 70, 120, 110, fill="lightgray", outline="")
    ]
    flakes = [canvas.create_text(x, 110, text="*", font=("Arial", 16), fill="white") for x in range(55, 110, 15)]
    def snow():
        for _ in range(10):
            for flake in flakes:
                canvas.move(flake, 0, 3)
            window.update()
            canvas.after(100)
            for flake in flakes:
                canvas.move(flake, 0, -3)
    canvas.after(100, snow)

def animate_fog():
    canvas.create_rectangle(20, 50, 130, 80, fill="gray", stipple="gray25", outline="")
    canvas.create_rectangle(30, 70, 120, 90, fill="lightgray", stipple="gray50", outline="")

# --- Placeholder Behavior ---
def on_entry_click(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter city name")
        city_entry.config(fg="gray")

# --- UI ---
window = tk.Tk()
window.title("Clima")
window.geometry("400x500")
window.configure(bg="#AED6F1")

frame = tk.Frame(window, bg="white", padx=20, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(frame, text="Clima", font=("Helvetica", 22, "bold"), bg="white", fg="#21618C")
title.pack(pady=(0, 20))

city_entry = tk.Entry(frame, font=("Arial", 14), width=25, justify="center", fg="gray")
city_entry.insert(0, "Enter city name")
city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focusout)
city_entry.pack(pady=10)

button = tk.Button(frame, text="Get Weather", font=("Arial", 12, "bold"),
                   bg="#3498DB", fg="white", activebackground="#2980B9",
                   padx=10, pady=5, command=get_weather)
button.pack(pady=10)

metric_var = tk.BooleanVar(value=False)
unit_toggle = tk.Checkbutton(frame, text="Use Metric (ºC)", variable=metric_var,
                             bg="white", font=("Arial", 10))
unit_toggle.pack(pady=5)

canvas = Canvas(frame, width=150, height=130, bg="white", highlightthickness=0)
canvas.pack(pady=5)

weather_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), bg="white")
weather_label.pack(pady=(5, 2))

temp_label = tk.Label(frame, text="", font=("Arial", 14), bg="white")
temp_label.pack()


window.mainloop()
