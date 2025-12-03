import customtkinter as ctk
from PIL import Image, ImageTk
import random
import os
import sys
import subprocess
import json 

root = ctk.CTk()
root.title("Patient data")
root.geometry("1366x768")
root.resizable(True, True)

# --- Load background image after root creation ---
bg_image = ctk.CTkImage(Image.open("vector-healthcare-medical-sciencefuturistic-background-260nw-2652074677.jpg"), size=(1366, 768))
bg_label = ctk.CTkLabel(root, text="", image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def go_back():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__),"Homepage.py")
    subprocess.Popen([sys.executable, file_path])


back_button = ctk.CTkButton(root, text="← Back", width=140, height=60, fg_color="#63B1F1",  text_color="black", font=("Arial", 20, "bold"), command=go_back)
back_button.place(x=70, y=30) 

ctk.CTkLabel(root, text="  All Registered Patients  ", fg_color="#63B1F1", width=300, height=80, text_color="black", font=("Arial", 30, "bold")).pack(pady=50)

# Scrollable frame
scroll = ctk.CTkScrollableFrame(root, fg_color="#d1d9e9", width=800, height=500)
scroll.pack(pady=10)

file_path = "patients.json"

# Load saved patients
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        patients = json.load(file)
else:
    patients = []

# Table headers
headers = ["Case ID", "Gender", "Age", "Height", "weight", "Temperature"]
for col, text in enumerate(headers):
    ctk.CTkLabel(scroll, text=text, font=("Arial", 25, "bold")) \
        .grid(row=0, column=col, padx=20, pady=10)

# Table rows
for row, p in enumerate(patients, start=1):
    ctk.CTkLabel(scroll, text=p["case_id"], font=("Arial", 16)) \
        .grid(row=row, column=0, padx=20, pady=5)
    ctk.CTkLabel(scroll, text=p["gender"], font=("Arial", 16)) \
        .grid(row=row, column=1, padx=20, pady=5)
    ctk.CTkLabel(scroll, text=p["age"], font=("Arial", 16)) \
        .grid(row=row, column=2, padx=20, pady=5)
    ctk.CTkLabel(scroll, text=p["height"], font=("Arial", 16)) \
        .grid(row=row, column=3, padx=20, pady=5)
    ctk.CTkLabel(scroll, text=p["weight"], font=("Arial", 16)) \
        .grid(row=row, column=4, padx=20, pady=5)
    ctk.CTkLabel(scroll, text=p["temperature"], font=("Arial", 16)) \
        .grid(row=row, column=5, padx=20, pady=5)
root.mainloop()