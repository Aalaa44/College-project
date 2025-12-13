"""
patient_insertion.py - Complete Working Version
VitalSignSim TSV File → GUI → XGBoost ML Model
"""

import customtkinter as ctk
from PIL import Image
import random
import os
import sys
import subprocess
import json
import threading
from datetime import datetime

# Try to import integration modules
try:
    from simulator_bridge import FileBasedSimulatorBridge
    SIMULATOR_AVAILABLE = True
except ImportError:
    print("Warning: simulator_bridge.py not found")
    SIMULATOR_AVAILABLE = False

try:
    from ml_model_handler import MLModelHandler
    ML_AVAILABLE = True
except ImportError:
    print("Warning: ml_model_handler.py not found")
    ML_AVAILABLE = False

# Global variables
simulator = None
simulator_active = False
ml_model = None
current_prediction = None
auto_update_active = False

# Create root window
root = ctk.CTk()
root.title("Patient Insertion")
root.geometry("1366x768")
root.resizable(True, True)

# Background
try:
    bg_image = ctk.CTkImage(
        Image.open("vector-healthcare-medical-sciencefuturistic-background-260nw-2652074677.jpg"),
        size=(1366, 768)
    )
    bg_label = ctk.CTkLabel(root, text="", image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    print("Background image not found")

# ==================== FUNCTIONS ====================

def initialize_ml_model():
    """Load ML model on startup"""
    global ml_model
    if ML_AVAILABLE:
        try:
            ml_model = MLModelHandler("risk_classifier_model.pkl")
            if ml_model.model:
                update_status("AI Model Ready", "green")
            else:
                update_status("Model file not found", "orange")
        except Exception as e:
            update_status(f"Model error: {str(e)[:30]}", "orange")

def initialize_simulator():
    """Connect to VitalSignSim via text file"""
    global simulator, simulator_active
    
    if not SIMULATOR_AVAILABLE:
        update_status("simulator_bridge.py missing", "red")
        return
    
    def connect_async():
        global simulator, simulator_active
        
        # Text file paths to try
        file_paths = [
            'vitalsign_output.txt',
            'simulator_output.txt',
            os.path.join(os.path.expanduser('~'), 'Documents', 'vitalsign_output.txt'),
        ]
        
        # Try each file path
        for file_path in file_paths:
            try:
                simulator = FileBasedSimulatorBridge(file_path)
                if simulator.connect():
                    simulator.start_monitoring(callback=on_simulator_data)
                    simulator_active = True
                    root.after(0, lambda fp=file_path: update_status(f"File: {os.path.basename(fp)}", "green"))
                    return
            except Exception as e:
                continue
        
        # If all failed
        root.after(0, lambda: update_status("No simulator file found", "orange"))
    
    threading.Thread(target=connect_async, daemon=True).start()

def on_simulator_data(vital_signs):
    """Callback when simulator sends new data"""
    root.after(0, lambda: update_vital_fields(vital_signs))

def update_vital_fields(vital_signs):
    """Update UI with simulator data"""
    if 'heart_rate' in vital_signs:
        hr_var.set(vital_signs['heart_rate'])
    if 'systolic_bp' in vital_signs:
        sys_var.set(vital_signs['systolic_bp'])
    if 'diastolic_bp' in vital_signs:
        dia_var.set(vital_signs['diastolic_bp'])
    if 'spo2' in vital_signs:
        spo2_var.set(vital_signs['spo2'])
    if 'respiratory_rate' in vital_signs:
        rr_var.set(vital_signs['respiratory_rate'])
    if 'temperature' in vital_signs:
        temp_var.set(vital_signs['temperature'])

def fetch_from_simulator():
    """Manual fetch button"""
    global simulator, simulator_active
    if not simulator_active:
        show_message("Simulator not connected", "orange")
        return
    
    data = simulator.get_latest_data()
    if data:
        update_vital_fields(data)
        show_message("Data fetched", "green")
    else:
        show_message("No data available", "orange")

def toggle_auto_update():
    """Toggle continuous updates"""
    global auto_update_active
    auto_update_active = not auto_update_active
    
    if auto_update_active:
        show_message("Auto-update ON", "blue")
        auto_update_loop()
    else:
        show_message("Auto-update OFF", "gray")

def auto_update_loop():
    """Continuously update from simulator"""
    global auto_update_active, simulator, simulator_active
    if auto_update_active and simulator_active:
        data = simulator.get_latest_data()
        if data:
            update_vital_fields(data)
        root.after(1000, auto_update_loop)

def run_ai_analysis():
    """Run ML prediction"""
    global ml_model, current_prediction
    
    if not ml_model or not ml_model.model:
        msg = "AI Model not loaded. Please add risk_classifier_model.pkl"
        show_message(msg, "orange")
        update_prediction_box(msg)
        return
    
    if not validate_inputs():
        return
    
    update_prediction_box("Running AI analysis...\nPlease wait...")
    
    def analyze():
        global current_prediction
        patient_data = collect_patient_data()
        result = ml_model.predict(patient_data)
        current_prediction = result
        root.after(0, lambda: display_prediction(result))
    
    threading.Thread(target=analyze, daemon=True).start()

def display_prediction(result):
    """Display AI results"""
    if not result or result.get('error'):
        update_prediction_box(f"Error: {result.get('error', 'Unknown')}")
        return
    
    output = f"""
╔══════════════════════════════════════════════════════════╗
║              AI RISK ASSESSMENT RESULTS                   ║
╚══════════════════════════════════════════════════════════╝

CLASSIFICATION: {result['risk_class']}
Risk Probability: {result['risk_probability_percent']}%
Model Confidence: {result['model_confidence']}
Status: {result['condition']}
Analysis Time: {result['predicted_at'][:19]}

CLINICAL ALERTS:
"""
    for i, alert in enumerate(result.get('alerts', []), 1):
        output += f"   {i}. {alert}\n"
    
    output += "\nRECOMMENDATIONS:\n"
    for i, rec in enumerate(result.get('recommendations', []), 1):
        output += f"   {i}. {rec}\n"
    
    update_prediction_box(output)
    
    # Update status message
    if result['severity'] == 'critical':
        show_message("CRITICAL RISK - Immediate Action Required!", "red")
    elif result['severity'] == 'monitor':
        show_message("Patient requires monitoring", "orange")
    else:
        show_message("Patient assessment complete", "green")

def validate_inputs():
    """Check required fields"""
    required = [
        (age_var.get(), "Age"),
        (height_var.get(), "Height"),
        (weight_var.get(), "Weight"),
        (temp_var.get(), "Temperature")
    ]
    
    for value, name in required:
        if not value or not value.strip():
            show_message(f"{name} is required", "red")
            return False
    return True

def collect_patient_data():
    """Gather all form data"""
    return {
        "case_id": case_id_var.get(),
        "gender": gender_var.get(),
        "age": age_var.get(),
        "height": height_var.get(),
        "weight": weight_var.get(),
        "temperature": temp_var.get(),
        "vital_signs": {
            "timestamp": datetime.now().isoformat(),
            "heart_rate": hr_var.get() or "0",
            "systolic_bp": sys_var.get() or "0",
            "diastolic_bp": dia_var.get() or "0",
            "spo2": spo2_var.get() or "0",
            "respiratory_rate": rr_var.get() or "0",
            "temperature": temp_var.get() or "0"
        }
    }

def save_patient():
    """Save to patients.json"""
    global current_prediction
    
    if not validate_inputs():
        return
    
    patient_data = collect_patient_data()
    
    # Add ML prediction if available
    if current_prediction:
        patient_data['ml_predictions'] = current_prediction
    
    # Load existing
    file_path = "patients.json"
    patients = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            patients = json.load(f)
    
    patients.append(patient_data)
    
    # Save
    with open(file_path, "w") as f:
        json.dump(patients, f, indent=4)
    
    show_message(f"Patient {patient_data['case_id']} saved!", "green")
    root.after(2000, clear_form)

def clear_form():
    """Reset all fields"""
    global current_prediction
    case_id_var.set(f"CASE-{random.randint(1000, 9999)}")
    gender_var.set("Male")
    age_var.set("")
    height_var.set("")
    weight_var.set("")
    temp_var.set("")
    hr_var.set("")
    sys_var.set("")
    dia_var.set("")
    spo2_var.set("")
    rr_var.set("")
    current_prediction = None
    update_prediction_box("Enter patient data and click 'Run AI Analysis'")
    show_message("", "")

def update_status(text, color):
    """Update status label"""
    if 'status_label' in globals():
        status_label.configure(text=text, text_color=color)

def show_message(text, color):
    """Display message"""
    message_label.configure(text=text, text_color=color)

def update_prediction_box(text):
    """Update prediction textbox"""
    prediction_box.configure(state="normal")
    prediction_box.delete("1.0", "end")
    prediction_box.insert("1.0", text)
    prediction_box.configure(state="disabled")

def go_back():
    """Return to homepage"""
    global simulator, auto_update_active
    auto_update_active = False
    if simulator and simulator_active:
        try:
            simulator.disconnect()
        except:
            pass
    root.destroy()
    file_path = os.path.join(os.path.dirname(__file__), "Homepage.py")
    subprocess.Popen([sys.executable, file_path])

# ==================== UI SETUP ====================

# Back button
back_button = ctk.CTkButton(
    root, text="← Back", width=140, height=60,
    fg_color="#63B1F1", text_color="black",
    font=("Arial", 20, "bold"), command=go_back
)
back_button.place(x=70, y=30)

# Title
title = ctk.CTkLabel(
    root, text="  Patient Insertion  ",
    fg_color="#63B1F1", width=300, height=80,
    text_color="black", font=("Arial", 30, "bold")
)
title.pack(pady=50)

# Main scrollable frame
scroll = ctk.CTkScrollableFrame(root, width=1000, height=550, fg_color="white")
scroll.pack(pady=10)

# Section 1: Demographics
demo_frame = ctk.CTkFrame(scroll, fg_color="#E8F4F8", corner_radius=10)
demo_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    demo_frame, text="Patient Demographics",
    font=("Arial", 22, "bold"), text_color="#1565C0"
).pack(pady=15)

# Case ID
case_id_var = ctk.StringVar(value=f"CASE-{random.randint(1000, 9999)}")
f = ctk.CTkFrame(demo_frame, fg_color="transparent")
f.pack(fill="x", padx=40, pady=5)
ctk.CTkLabel(f, text="Case ID:", font=("Arial", 18, "bold"), width=200, anchor="w").pack(side="left")
ctk.CTkEntry(f, textvariable=case_id_var, width=350, font=("Arial", 16), state="readonly").pack(side="left", padx=20)

# Gender
gender_var = ctk.StringVar(value="Male")
f = ctk.CTkFrame(demo_frame, fg_color="transparent")
f.pack(fill="x", padx=40, pady=5)
ctk.CTkLabel(f, text="Gender:", font=("Arial", 18, "bold"), width=200, anchor="w").pack(side="left")
ctk.CTkRadioButton(f, text="Male", variable=gender_var, value="Male", font=("Arial", 16)).pack(side="left", padx=20)
ctk.CTkRadioButton(f, text="Female", variable=gender_var, value="Female", font=("Arial", 16)).pack(side="left", padx=20)

# Age, Height, Weight
age_var = ctk.StringVar()
height_var = ctk.StringVar()
weight_var = ctk.StringVar()

for label, var in [("Age (years):", age_var), ("Height (cm):", height_var), ("Weight (kg):", weight_var)]:
    f = ctk.CTkFrame(demo_frame, fg_color="transparent")
    f.pack(fill="x", padx=40, pady=5)
    ctk.CTkLabel(f, text=label, font=("Arial", 18, "bold"), width=200, anchor="w").pack(side="left")
    ctk.CTkEntry(f, textvariable=var, width=350, font=("Arial", 16)).pack(side="left", padx=20)

# Section 2: Vital Signs
vital_frame = ctk.CTkFrame(scroll, fg_color="#FFF4E6", corner_radius=10)
vital_frame.pack(fill="x", padx=20, pady=10)

header = ctk.CTkFrame(vital_frame, fg_color="transparent")
header.pack(fill="x", pady=10)
ctk.CTkLabel(header, text="Vital Signs", font=("Arial", 22, "bold"), text_color="#E65100").pack(side="left", padx=20)

status_label = ctk.CTkLabel(header, text="Initializing...", font=("Arial", 14), text_color="gray")
status_label.pack(side="right", padx=20)

# Vital signs inputs
temp_var = ctk.StringVar()
hr_var = ctk.StringVar()
sys_var = ctk.StringVar()
dia_var = ctk.StringVar()
spo2_var = ctk.StringVar()
rr_var = ctk.StringVar()

vital_fields = [
    ("Temperature (C):", temp_var, "36.5-37.5"),
    ("Heart Rate (bpm):", hr_var, "60-100"),
    ("Systolic BP:", sys_var, "90-120"),
    ("Diastolic BP:", dia_var, "60-80"),
    ("SpO2 (%):", spo2_var, ">95"),
    ("Respiratory Rate:", rr_var, "12-20")
]

for label, var, hint in vital_fields:
    f = ctk.CTkFrame(vital_frame, fg_color="transparent")
    f.pack(fill="x", padx=40, pady=5)
    label_container = ctk.CTkFrame(f, fg_color="transparent")
    label_container.pack(side="left")
    ctk.CTkLabel(label_container, text=label, font=("Arial", 18, "bold"), width=200, anchor="w").pack()
    ctk.CTkLabel(label_container, text=hint, font=("Arial", 11), text_color="gray", anchor="w").pack()
    ctk.CTkEntry(f, textvariable=var, width=350, font=("Arial", 16)).pack(side="left", padx=20)

# Simulator buttons
btn_frame = ctk.CTkFrame(vital_frame, fg_color="transparent")
btn_frame.pack(pady=15)
ctk.CTkButton(
    btn_frame, text="Fetch from Simulator",
    fg_color="#4CAF50", width=220, height=45,
    font=("Arial", 16, "bold"), command=fetch_from_simulator
).grid(row=0, column=0, padx=10)
ctk.CTkButton(
    btn_frame, text="Auto-Update",
    fg_color="#2196F3", width=180, height=45,
    font=("Arial", 16, "bold"), command=toggle_auto_update
).grid(row=0, column=1, padx=10)

# Section 3: AI Analysis
ai_frame = ctk.CTkFrame(scroll, fg_color="#F3E5F5", corner_radius=10)
ai_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(
    ai_frame, text="AI Risk Assessment",
    font=("Arial", 22, "bold"), text_color="#6A1B9A"
).pack(pady=15)

prediction_box = ctk.CTkTextbox(ai_frame, width=900, height=180, font=("Courier", 13))
prediction_box.pack(padx=20, pady=10)
prediction_box.insert("1.0", "Enter patient data and click 'Run AI Analysis'")
prediction_box.configure(state="disabled")

ctk.CTkButton(
    ai_frame, text="Run AI Analysis",
    fg_color="#9C27B0", width=250, height=50,
    font=("Arial", 18, "bold"), command=run_ai_analysis
).pack(pady=15)

# Action buttons
action_frame = ctk.CTkFrame(scroll, fg_color="transparent")
action_frame.pack(pady=20)
ctk.CTkButton(
    action_frame, text="Save Patient",
    fg_color="#2196F3", width=220, height=55,
    font=("Arial", 20, "bold"), command=save_patient
).grid(row=0, column=0, padx=15)
ctk.CTkButton(
    action_frame, text="Clear Form",
    fg_color="#FF9800", width=220, height=55,
    font=("Arial", 20, "bold"), command=clear_form
).grid(row=0, column=1, padx=15)

# Message label
message_label = ctk.CTkLabel(scroll, text="", font=("Arial", 16, "bold"))
message_label.pack(pady=10)

# ==================== INITIALIZATION ====================

# Initialize on startup
root.after(100, initialize_ml_model)
root.after(200, initialize_simulator)

# ==================== RUN ====================

root.mainloop()