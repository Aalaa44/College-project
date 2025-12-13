import customtkinter as ctk
from PIL import Image
import random
import os
import sys
import subprocess
import matplotlib
matplotlib.use("Agg")   # Prevent backend issues
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- Create root window ---
root = ctk.CTk()
root.title("Analysis Report")
root.geometry("1920x1080")
root.resizable(True, True)

# ------------------ MAIN BACKGROUND ------------------
#bg_image = ctk.CTkImage(Image.open("Image (27).jfif"), size=(1920, 1080))
#bg_label = ctk.CTkLabel(root, text="", image=bg_image)
bg_label = ctk.CTkLabel(root, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()


# ----------------------------------------------------------
# --- SCROLLABLE FRAME (CONTENT AREA) ----------------------
# ----------------------------------------------------------
content = ctk.CTkScrollableFrame(root, width=1800, height=900)
content.pack(fill="both", expand=True, pady=0)

# ---- Background *inside* scrollable frame ----
scroll_bg_image = ctk.CTkImage(Image.open("Image (27).jfif"), size=(1920,1080))
scroll_bg_label = ctk.CTkLabel(content, image=scroll_bg_image, text="")
scroll_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
scroll_bg_label.lower()


# --- Back Button ---
def go_back():
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "homepage 1.py")
    subprocess.Popen([sys.executable, file_path])

back_button = ctk.CTkButton(root, text="← Back", width=140, height=60,
                            fg_color="#63B1F1", text_color="black",
                            font=("Arial", 20, "bold"), command=go_back)
back_button.place(x=70, y=30)

# ------------------ Title ------------------
title_label = ctk.CTkLabel(content, text="Analysis Report", fg_color="#63B1F1",
                           width=300, height=80, text_color="black",
                           font=("Arial", 30, "bold"))
title_label.pack(pady=20)

# ------------------ Case ID ------------------
case_frame = ctk.CTkFrame(content, corner_radius=25, fg_color="transparent")
case_frame.pack(padx=200, pady=20)

ctk.CTkLabel(case_frame, text="Case ID:", font=("Arial", 20, "bold"),
             width=150, height=70).pack(side="left", padx=10)

generated_case_id = "CASE-" + str(random.randint(1000, 9999))

case_entry = ctk.CTkEntry(case_frame, width=200, font=("Arial", 16))
case_entry.pack(side="left")
case_entry.insert(0, generated_case_id)
case_entry.configure(state="readonly")

# --------------------------------------------------------------------
# ------------------ RANDOM CURVE GRAPH SECTION ----------------------
# --------------------------------------------------------------------
graph_frame = ctk.CTkFrame(content, width=800, height=400, corner_radius=20, fg_color="#ffffff")
graph_frame.pack(pady=20)

x = list(range(50))
y = [random.randint(0, 100) for _ in x]

fig = Figure(figsize=(6, 3), dpi=100)
plot1 = fig.add_subplot(111)
plot1.plot(x, y, color="blue", linewidth=2)
plot1.set_title("Random Curve")
plot1.set_xlabel("X Values")
plot1.set_ylabel("Y Values")

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(pady=10)

# ------------------ Gender ------------------
gender_frame = ctk.CTkFrame(content, corner_radius=25, fg_color="transparent")
gender_frame.pack(padx=200, pady=20)

ctk.CTkLabel(gender_frame, text="Gender:", font=("Arial", 20, "bold"),
             width=150, height=70).pack(side="left", padx=10)

gender_var = ctk.StringVar(value="Male")

ctk.CTkRadioButton(gender_frame, text="Male", font=("Arial", 17),
                   variable=gender_var, value="Male").pack(side="left", padx=5)
ctk.CTkRadioButton(gender_frame, text="Female", font=("Arial", 17),
                   variable=gender_var, value="Female").pack(side="left", padx=5)

# ------------------ Age Slider ------------------
age_frame = ctk.CTkFrame(content, corner_radius=25, fg_color="transparent")
age_frame.pack(padx=150, pady=20)

ctk.CTkLabel(age_frame, text="Age:", font=("Arial", 20, "bold"),
             width=150, height=70).pack(side="left", padx=10)

age_value = ctk.StringVar(value="25")

def update_age(value):
    age_value.set(str(int(float(value))))

age_slider = ctk.CTkSlider(age_frame, from_=1, to=100, command=update_age)
age_slider.set(25)
age_slider.pack(side="left", padx=10)

age_label = ctk.CTkLabel(age_frame, textvariable=age_value, font=("Arial", 16))
age_label.pack(side="left")

# --- Footer Label ---
footer_label = ctk.CTkLabel(
    content,
    text="Designed By Alaa&Esraa - All Copyrights Reserved 2025",
    font=("Arial", 12, "italic"),
    text_color="black"
)
footer_label.pack(pady=40)

# run the app
root.mainloop()
