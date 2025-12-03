import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
import json
import subprocess

# --- Create root window first ---
root = ctk.CTk()
root.title("Delete Patient")
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


# ------------------ Title ------------------
title_label = ctk.CTkLabel(root, text="  Delete Patient Record  ", fg_color="#63B1F1", width=300, height=80, text_color="black", font=("Arial", 30, "bold"))
title_label.pack(pady=70)


# --- Input Frame ---
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(pady=10)

ctk.CTkLabel(frame, text="Enter Case ID:", font=("Arial", 20, "bold"), width=150, height=70).pack(side="left", padx=10)
case_entry = ctk.CTkEntry(frame, width=250, font=("Arial", 18))
case_entry.pack(side="left", padx=10)

# --- Message Label ---
message_label = ctk.CTkLabel(root, text="", font=("Arial", 18), text_color="red")
message_label.pack(pady=20)

# --- Delete Function ---
def delete_patient():
    case_id = case_entry.get().strip()
    file_path = "patients.json"

    # No ID entered
    if not case_id:
        message_label.configure(text="⚠ Please enter a Case ID", text_color="red")
        return

    # If file does not exist
    if not os.path.exists(file_path):
        message_label.configure(text="No patient records found!", text_color="red")
        return

    # Load existing data
    with open(file_path, "r") as file:
        patients = json.load(file)

    # Try deleting
    deleted = False
    new_list = []

    for p in patients:
        if p["case_id"] == case_id:
            deleted = True    # Found -> delete
        else:
            new_list.append(p)

    if not deleted:
        message_label.configure(text=f"❌ Case ID '{case_id}' not found!", text_color="red")
        return

    # Save updated data
    with open(file_path, "w") as file:
        json.dump(new_list, file, indent=4)

    message_label.configure(text=f"✔ Patient '{case_id}' deleted successfully!", text_color="green")
    case_entry.delete(0, "end")


# --- Delete Button ---
ctk.CTkButton(
    root,
    text="Delete",
    fg_color="#FF5C5C",
    hover_color="#FF7878",
    width=200,
    height=50,
    font=("Arial", 22, "bold"),
    command=delete_patient
).pack(pady=20)

root.mainloop()