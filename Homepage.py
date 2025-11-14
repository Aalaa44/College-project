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
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "waiting.py")
    subprocess.Popen([sys.executable, file_path])

def open_patient_data():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "waiting.py")
    subprocess.Popen([sys.executable, file_path])

def open_analysis_report():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "waiting.py")
    subprocess.Popen([sys.executable, file_path])

def open_copyrights():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "waiting.py")
    subprocess.Popen([sys.executable, file_path])


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
title_label = tk.Label(root, text="Home Page", font=("Arial", 48, "bold"),bg=bg_label.cget("background"), fg="#2596be")
title_label.pack(pady=40)

# --- Buttons (each with its own command) ---
btn_style = {"width": 20, "height": 2, "font": ("Arial", 14, "bold"), "bg": "#69b9de"}

btn_insert = tk.Button(root, text="Patients insertion", **btn_style, command=open_patient_insertion)
btn_insert.pack(pady=10)

btn_page = tk.Button(root, text="Patients Page", **btn_style, command=open_patient_page)
btn_page.pack(pady=10)

btn_data = tk.Button(root, text="Patients data", **btn_style, command=open_patient_data)
btn_data.pack(pady=10)

btn_report = tk.Button(root, text="Analysis report", **btn_style, command=open_analysis_report)
btn_report.pack(pady=10)

btn_copy = tk.Button(root, text="Copyrights", **btn_style, command=open_copyrights)
btn_copy.pack(pady=10)

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