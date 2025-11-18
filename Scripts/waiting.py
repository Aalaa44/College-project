import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys

# ---------- FUNCTIONS ----------
def open_patient_insertion():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "Patient insertion.py")
    subprocess.Popen([sys.executable, file_path])

def open_patient_page():
    print("Opening Patients Page... (not yet linked)")

def open_patient_data():
    print("Opening Patients Data... (not yet linked)")

def open_analysis_report():
    print("Opening Analysis Report... (not yet linked)")

def open_copyrights():
    print("Showing Copyrights... (not yet linked)")


# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Home Page")
root.geometry("1366x768")
root.resizable(True, True)

# --- Background ---
bg_image = Image.open("hp-bg.jpg").resize((1366, 768))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Title Label ---
title_label = tk.Label(root, text="لسه شغالين عليهااااااااااااا", font=("Arial", 48, "bold"), bg=bg_label.cget("background"), fg="#2596be")
title_label.pack(pady=40)


# Load image using Pillow
image_path = "loading.jpg"   # <-- change this to your image file path
img = Image.open(image_path)
img = img.resize((100, 100))  # resize to fit window

# Convert to Tkinter-compatible format
photo = ImageTk.PhotoImage(img)

# Display image inside a Label
label = tk.Label(root, image=photo)
label.pack(fill="both", expand=False)






def go_back():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__),"Homepage.py")
    subprocess.Popen([sys.executable, file_path])

btn_style = {"width": 20, "height": 2, "font": ("Arial", 14, "bold"), "bg": "#69b9de"}

btn_insert = tk.Button(root, text="اهرررررب", **btn_style, command=go_back)
btn_insert.pack(pady=10)


# --- Footer Label ---
footer_label = tk.Label(root,
    text="Designed By Alaa&Esraa - All Copyrights Reserved 2025",
    font=("Arial", 12, "italic"),
    anchor="w",
    justify="left",
    bg=bg_label.cget("background"),
    fg="white"
)
footer_label.pack(side="bottom", fill="x", padx=10, pady=0)

# --- Run the App ---
root.mainloop()