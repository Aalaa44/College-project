import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import sys
import subprocess


# --- Create root window first ---
root = tk.Tk()
root.title("Patient insertion")
root.geometry("1366x768")
root.resizable(True, True)

# --- Load background image after root creation ---
bg_image = Image.open("hp-bg.jpg")
bg_image = bg_image.resize((1366, 768))
bg_photo = ImageTk.PhotoImage(bg_image)

# --- Display background image ---
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def go_back():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__),"Homepage.py")
    subprocess.Popen([sys.executable, file_path])

back_button = tk.Button(root, text= "← Back",font=("Arial", 14, "bold"), fg="black", bg=bg_label.cget("background"), command=go_back)
back_button.place(x=20, y=20)


frame = tk.Frame(root,  bg=bg_label.cget("background"), padx=30, pady=30)
frame.pack(pady=20)


# case id
case_id = f"CASE-{random.randint(1000, 9999)}"
tk.Label(frame, text="Case ID:", font=("Arial", 14, "bold"), bg=bg_label.cget("background"), foreground= "#2596be").grid(row=0, column=0, sticky="w", pady=10)
case_entry = tk.Entry(frame, font=("Arial", 14), width=20)
case_entry.grid(row=0, column=1, pady=10)
case_entry.insert(0, case_id)
case_entry.config(state="readonly")


#gender
tk.Label(frame, text="Gender:", font=("Arial", 14, "bold"), bg=bg_label.cget("background"), foreground= "#2596be").grid(row=2, column=0, sticky="w", pady=10)
gender_var = tk.StringVar(value="Male")
gender_frame = tk.Frame(frame,bg=bg_label.cget("background"))
gender_frame.grid(row=2, column=1, sticky="w")
tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male",bg=bg_label.cget("background"), foreground= "#000000", font=("Arial", 12)).pack(side="left", padx=5)
tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female",bg=bg_label.cget("background"), foreground= "#000000", font=("Arial", 12)).pack(side="left", padx=5)


#age
tk.Label(frame, text="Age:", font=("Arial", 14, "bold"), bg=bg_label.cget("background"), foreground= "#2596be").grid(row=4, column=0, sticky="w", pady=10)
age_slider = tk.Scale(frame, from_=1, to=50, orient="horizontal", length=300, bg="#2596be")
age_slider.grid(row=4, column=1, pady=10, sticky="w")

#chronic diseases
#tk.Label(frame, text="Diseases:", font=("Arial", 14, "bold"), bg=bg_label.cget("background"), foreground= "#2596be").grid(row=6, column=0, sticky="w", pady=10)
#diseases = ["Diabetes","Immune conditions", "Cardiovascular", "Asthma"]
#diseases_var = []
#for i , diseases in enumerate(diseases):
#    var = tk.BooleanVar()
#    chk = tk.Checkbutton(frame,text =diseases, variable = var, bg=bg_label.cget("background"), font=("Arial",12))
#    chk.grid(row=6+2*i, column=1, sticky="w", padx=10, pady=2)
#    diseases_var.append(var)


#diagnosis
#tk.Label(frame, text="Diagnosis:", font=("Arial", 14, "bold"), bg=bg_label.cget("background"), foreground= "#2596be").grid(row=14, column=0, sticky="w", pady=10)
#dig_frame = tk.Frame(frame,bg=bg_label.cget("background"))
#dig_frame.grid(row=16, column=1, sticky="w")
#dig_var = tk.StringVar(value = "good")
#for i, option in enumerate(["Excellent", "Bad", "Died", "Good"]):
#    rad = tk.Radiobutton(frame, text=option, variable=dig_var, value=option, bg=bg_label.cget("background"), font=("Arial", 12))
#    rad.grid(row = 16+2*i, column=1, sticky="w",padx=10, pady=2)




#final buttons
button_frame = tk.Frame(frame, bg=bg_label.cget("background"))
button_frame.grid(row=24, column=1, sticky="e", pady=20)

def clear_choices():
    age_slider.set(1)
    gender_var.set("Male")
    #for var in diseases_var:
    #    var.set(False)
    #dig_var.set("Excellent")

cancel_btn = tk.Button(button_frame, text="Cancel", font=("Arial", 14, "bold"), bg="#f44336", fg="white", width=12, command=clear_choices)
cancel_btn.pack(side="left", padx=10)

submit_btn = tk.Button(button_frame, text="Submit", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=12)
submit_btn.pack(side="left", padx=10)



# --- Footer label ---
footer_label = tk.Label(root,
    text="Designed By Alaa&Esraa - All Copyrights Reserved 2025",
    font=("Arial", 12, "italic"),
    anchor="w",
    justify="left",
    bg=bg_label.cget("background")
)
footer_label.pack(side="bottom", fill="x", padx=10, pady=0)

# --- Run the app ---
root.mainloop()