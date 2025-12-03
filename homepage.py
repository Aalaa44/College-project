import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys

# ---------- FUNCTIONS ----------
def open_patient_insertion():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "patient_insertion.py")
    subprocess.Popen([sys.executable, file_path])

def open_delete_patient():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "delete_patient.py")
    subprocess.Popen([sys.executable, file_path])

def open_patient_data():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "patients_data.py")
    subprocess.Popen([sys.executable, file_path])

def open_analysis_report():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "Report.py")
    subprocess.Popen([sys.executable, file_path])

def open_copyrights():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "waiting.py")
    subprocess.Popen([sys.executable, file_path])


# ---------- MAIN WINDOW ----------
root = ctk.CTk()
root.title("Home Page")
root.geometry("1366x768")
root.resizable(True, True)

# --- Background ---
bg_image = ctk.CTkImage(Image.open("vector-healthcare-medical-sciencefuturistic-background-260nw-2652074677.jpg"), size=(1366, 768))
bg_label = ctk.CTkLabel(root, text="", image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Title Label ---
title_label = ctk.CTkLabel(root, text="Home Page", fg_color="#a1c1fc", width=400, height=100, text_color="black", font=("Arial", 48, "bold"))
title_label.pack(pady=40)

# --- Buttons (each with its own command) ---
btn_style = {"width": 350, "height": 70, "corner_radius": 25, "font": ("Arial", 22, "bold"), "fg_color": "#9abaff", "hover_color": "#97c9ff", "text_color": "black"  }

ctk.CTkButton(root, text="Patients insertion",command=lambda: open_patient_insertion(), **btn_style).pack(pady=10)

ctk.CTkButton(root, text="Delete Patient",command=lambda: open_delete_patient(), **btn_style).pack(pady=10)

ctk.CTkButton(root, text="Patients data",command=lambda: open_patient_data(), **btn_style).pack(pady=10)

ctk.CTkButton(root, text="Analysis report",command=lambda: open_analysis_report(), **btn_style).pack(pady=10)

ctk.CTkButton(root, text="Copyrights",command=lambda: open_copyrights(), **btn_style).pack(pady=10)

# --- Footer Label ---
footer_label = ctk.CTkLabel(root,
    text="Designed By Alaa&Esraa - All Copyrights Reserved 2025",
    font=("Arial", 12, "italic"),
    text_color="black"
)
footer_label.pack(side="bottom", fill="x", padx=10, pady=0)

# --- Run the App ---
root.mainloop()