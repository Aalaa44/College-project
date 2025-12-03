import customtkinter as ctk
from PIL import Image, ImageTk
import random
import os
import sys
import subprocess
import re
import math
import csv
from tkinter import messagebox
from striprtf.striprtf import rtf_to_text
from typing import List, Dict, Optional

# --- Create root window first ---
root = ctk.CTk()
root.title("Patient insertion")
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
title_label = ctk.CTkLabel(root, text="  Insert Patient Information  ", fg_color="#63B1F1", width=300, height=80, text_color="black", font=("Arial", 30, "bold"))
title_label.pack(pady=20)

# ------------------ Generate Case ID ------------------
generated_case_id = f"CASE-{random.randint(1000, 9999)}"

# ------------------ Case ID ------------------
case_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
case_frame.pack(padx=200, pady=20)

ctk.CTkLabel(case_frame, text="Case ID:", font=("Arial", 20, "bold"), width= 150, height= 70).pack(side="left", padx=10)

case_entry = ctk.CTkEntry(case_frame, width=200, font=("Arial", 16))
case_entry.pack(side="left")
case_entry.insert(0, generated_case_id)
case_entry.configure(state="readonly")  # cannot edit


# ------------------ Gender ------------------
gender_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
gender_frame.pack(padx=200, pady=15)

ctk.CTkLabel(gender_frame, text="Gender:", font=("Arial", 20, "bold"), width= 150, height= 70).pack(side="left", padx=10)

gender_var = ctk.StringVar(value="Male")

ctk.CTkRadioButton(gender_frame, text="Male", font=("Arial", 17), variable=gender_var, value="Male").pack(side="left", padx=5)
ctk.CTkRadioButton(gender_frame, text="Female", font=("Arial", 17), variable=gender_var, value="Female").pack(side="left", padx=5)



# ------------------ Age Slider ------------------

age_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
age_frame.pack(padx=150, pady=5)

ctk.CTkLabel(age_frame, text="Age:", font=("Arial", 20, "bold"), width= 150, height= 70).pack(side="left", padx=10)

age_value = ctk.StringVar(value="25")

def update_age(value):
    age_value.set(str(int(float(value))))

age_slider = ctk.CTkSlider(age_frame, from_=1, to=100, command=update_age)
age_slider.set(25)
age_slider.pack(side="left", padx=10)

age_label = ctk.CTkLabel(age_frame, textvariable=age_value, font=("Arial", 16))
age_label.pack(side="left")


# ----------------- Height -------------------
H_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
H_frame.pack(padx=150, pady=5)

ctk.CTkLabel(H_frame, text="Enter Height:", font=("Arial", 20, "bold"), width=150, height=70).pack(side="left", padx=10)
H_entry = ctk.CTkEntry(H_frame, width=250, font=("Arial", 18))
H_entry.pack(side="left", padx=10)

# ----------------- weight -------------------
W_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
W_frame.pack(padx=150, pady=5)

ctk.CTkLabel(W_frame, text="Enter Weight:", font=("Arial", 20, "bold"), width=150, height=70).pack(side="left", padx=10)
W_entry = ctk.CTkEntry(W_frame, width=250, font=("Arial", 18))
W_entry.pack(side="left", padx=10)

# ----------------- Temperature -------------------
T_frame = ctk.CTkFrame(root, corner_radius=25, fg_color="transparent")
T_frame.pack(padx=150, pady=5)

ctk.CTkLabel(T_frame, text="Enter Temperature:", font=("Arial", 20, "bold"), width=150, height=70).pack(side="left", padx=10)
T_entry = ctk.CTkEntry(T_frame, width=250, font=("Arial", 18))
T_entry.pack(side="left", padx=10)



# --- CONFIGURATION ---
RTF_FILE_PATH = r"D:\trying\College-project\Scripts\try.rtf"

# ----------------------------------------------------
# 1. Parsing Functions (Restored to original structure)
# ----------------------------------------------------

def is_time(value: str) -> bool:
    """Checks if a string matches the XX:XX time pattern."""
    return re.match(r"^\d{2}:\d{2}$", value)

def parse_table(text: str) -> Optional[List[Dict[str, str]]]:
    """
    Uses a robust regex pattern to extract all rows based on the 7 fixed fields,
    followed by the variable-length Event.
    """
    
    # 1. Cleaning and Preparation
    # Convert RTF to clean text, removing all RTF commands { \ } and collapsing whitespace
    clean_text = re.sub(r"[{}\t]", " ", text) 
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    
    # Define the core pattern to capture one row:
    # 1. Time (HH:MM) - (\d{2}:\d{2})
    # 2. 6 Fixed Fields (HR, SpO2, etCO2, RR, NIBP, Rhythm) - (\S+)
    # 3. Event Text (everything until the next Time) - (.*?)
    #    The '.*?' is non-greedy, stopping before the next Time pattern.
    
    # Look for Time followed by 6 other non-whitespace tokens, 
    # then the rest of the line until the next time pattern.
    row_pattern = re.compile(
        r"(\d{2}:\d{2})\s+"         # Time
        r"(\S+)\s+"                 # HR
        r"(\S+)\s+"                 # SpO2
        r"(\S+)\s+"                 # etCO2
        r"(\S+)\s+"                 # RR
        r"(\S+)\s+"                 # NIBP
        r"(\S+)"                    # Rhythm
        r"(.*?)"                    # Event (non-greedy capture until next timestamp or EOF)
        r"(?=\s*\d{2}:\d{2}|\s*$)", # Positive Lookahead: Next pattern is Time or End of String
        re.DOTALL | re.IGNORECASE   # DOTALL lets '.' match newlines, making it robust
    )

    matches = row_pattern.finditer(clean_text)
    rows = []
    
    for match in matches:
        # The Event text captured by group(8) may contain leading/trailing spaces, so strip it.
        event_val = match.group(8).strip()
        
        rows.append({
            "Time": match.group(1),
            "HR": match.group(2),
            "SpO2": match.group(3),
            "etCO2": match.group(4),
            "RR": match.group(5),
            "NIBP": match.group(6),
            "Rhythm": match.group(7),
            "Event": event_val, 
        })

    if not rows:
        print("\n[DEBUG] Regex found no matching rows. Check RTF table formatting.")
        
    return rows if rows else None

# ----------------------------------------------------
# 2. Auxiliary Calculation Functions
# ----------------------------------------------------

def calculate_map(systolic: int, diastolic: int) -> str:
    """
    Calculates Mean Arterial Pressure (MAP).
    """
    try:
        pp_calc = systolic - diastolic
        map_calc = round(diastolic + (1/3) * pp_calc)
        return str(map_calc)
    except Exception:
        return "Error"

def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """
    Calculates Body Mass Index (BMI).
    """
    if height_m <= 0:
        return "Error: Height zero"
    try:
        # Ensure standard float division is used here:
        bmi_calc = weight_kg / math.pow(height_m, 2)
        return bmi_calc
    except Exception:
        return "Error"

# ----------------------------------------------------
# 3. Primary Calculation Function (Vitals + BMI)
# ----------------------------------------------------

def calculate_vitals_and_bmi(rows: List[Dict[str, str]], weight: float, height: float, temp: float) -> List[Dict[str, str]]:
    """
    Calculates PP, MAP, and BMI for each row, adding static patient data.
    """
    print("Calculating PP, MAP, and BMI...")
    
    bmi_val = calculate_bmi(weight, height)

    for row in rows:
        # Add static patient data
        row["Weight(kg)"] = str(weight)
        row["Height(m)"] = str(height)
        row["Temp(C)"] = str(temp)
        row["BMI"] = bmi_val
        
        # --- NIBP Calculations (PP & MAP) ---
        nibp = row.get("NIBP", "")
        pp = "Error"
        map_val = "Error"
        
        try:
            if "/" in nibp:
                systolic, diastolic = map(int, nibp.split("/"))
                
                pp = str(systolic - diastolic)
                map_val = calculate_map(systolic, diastolic)
        except ValueError:
            pass # Keep default 'Error' value
        
        # --- Update Row ---
        row["PP"] = pp
        row["MAP"] = map_val
    
    return rows

# ----------------------------------------------------
# 4. Save Function (CSV Export)
# ----------------------------------------------------

def save_calculated_data_to_csv(updated_rows: List[Dict[str, str]], original_path: str):
    """
    Saves the processed data, including all calculated fields, to a new CSV file.
    """
    if not updated_rows:
        print("[ERROR] No data rows to save.")
        return
        
    base, _ = os.path.splitext(original_path)
    output_path = base + "_processed.csv"
    
    print(f"Saving calculated data to CSV file: {output_path}")

    # Determine headers (keys) from the first row
    fieldnames = list(updated_rows[0].keys()) 

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        print(f"[SUCCESS] Calculated data saved to: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Failed to write CSV file: {e}")


# ----------------------------------------------------
# 5. Main Execution
# ----------------------------------------------------

def process_rtf_automatically(path: str, weight: float, height: float, temp: float):
    """Orchestrates the entire automated process."""
    if not os.path.exists(path):
        print(f"X ERROR: File not found at path: {path}")
        return

    print(f"Starting process for file: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            rtf_original_content = f.read() 
    except Exception as e:
        print(f"ERROR: Could not read RTF file: {e}")
        return

    text = rtf_to_text(rtf_original_content)

    # Parse into rows
    rows = parse_table(text)
    if not rows:
        print("ERROR: Could not parse time-series data from RTF content.")
        return

    print(f"Found {len(rows)} data records.")

    # Calculate Vitals (PP & MAP) and BMI, merging static data
    updated_rows = calculate_vitals_and_bmi(rows, weight, height, temp)

    # Save Updated Data to a clean CSV file
    save_calculated_data_to_csv(updated_rows, path)





# ------------------ Submit & Cancel ------------------

def clear_all():
    age_slider.set(25)
    age_value.set("25")

import json
def submit_data():
    """
    Handles data validation, calculation, submission, and RTF processing.
    """
    
    # 1. Get raw string inputs
    height_str = H_entry.get()
    weight_str = W_entry.get()
    temp_str = T_entry.get()

    # 2. VALIDATION & CONVERSION
    if not weight_str or not height_str or not temp_str:
        messagebox.showerror("Input Error", "Please enter values for Weight, Height, and Temperature.")
        return 

    try:
        final_weight = float(weight_str)
        final_height = float(height_str)
        final_temp = float(temp_str)
    except ValueError:
        messagebox.showerror("Input Error", "Weight, Height, and Temperature must be valid numbers.")
        return

    # 3. RTF PROCESSING & CALCULATIONS (The new, corrected step)
    process_rtf_automatically(
        RTF_FILE_PATH, 
        final_weight, 
        final_height, 
        final_temp
    )

    # 4. JSON SUBMISSION (saving the patient record)
    patient_data = {
        "case_id": case_entry.get(),
        "gender": gender_var.get(),
        "age": age_value.get(),
        "height": height_str,
        "weight": weight_str,
        "temperature": temp_str
    }

    file_path = "patients.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
             data = []
    else:
        data = []

    data.append(patient_data)

    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print("Patient Saved:", patient_data)
        messagebox.showinfo("Success", "Patient data submitted and calculations saved to CSV.") # Added success message
    except Exception as e:
        messagebox.showerror("JSON Error", f"Failed to save patient data: {e}")

    # 5. UI Cleanup (Reset for next patient)
    clear_all()
    # Regenerate Case ID
    case_entry.configure(state="normal")
    case_entry.delete(0, ctk.END)
    case_entry.insert(0, f"CASE-{random.randint(1000, 9999)}")
    case_entry.configure(state="readonly")


submit_frame = ctk.CTkFrame(root)
submit_frame.pack(pady=20)

ctk.CTkButton(submit_frame, text="Cancel", width=150, height=40, font=("Arial", 20), command=clear_all).pack(side="left", padx=0)
ctk.CTkButton(submit_frame, text="Submit", width=150, height=40, font=("Arial", 20), command=submit_data).pack(side="left", padx=0)

# --- Footer Label ---
footer_label = ctk.CTkLabel(root,
    text="Designed By Alaa&Esraa - All Copyrights Reserved 2025",
    font=("Arial", 12, "italic"),
    text_color="black"
)
footer_label.pack(side="bottom", fill="x", padx=10, pady=0)





# ------------------ Run App ------------------

root.mainloop()