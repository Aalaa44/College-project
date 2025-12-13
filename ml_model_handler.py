"""
ML Model Handler for XGBoost Risk Classification
FIXED to match your actual training feature names
"""

import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime
import os


class MLModelHandler:
    def __init__(self, model_path="risk_classifier_model.pkl"):
        """
        Initialize XGBoost model for risk prediction
        
        Expected features from YOUR training:
        - Patient ID
        - Heart Rate
        - Respiratory Rate
        - Body Temperature
        - Oxygen Saturation
        - Systolic Blood Pressure
        - Diastolic Blood Pressure
        - Age
        - Weight (kg)
        - Height (m)
        - Derived_Pulse_Pressure
        - Derived_BMI
        - Derived_MAP
        - Gender_Male
        """
        self.model_path = model_path
        self.model = None
        self.feature_names = None
        self.preprocessing_info = None
        self.load_model()
    
    def load_model(self):
        """Load the trained XGBoost model"""
        try:
            # Load model
            if not os.path.exists(self.model_path):
                print(f"Model file not found: {self.model_path}")
                return False
            
            self.model = joblib.load(self.model_path)
            print(f"✓ Model loaded from {self.model_path}")
            
            # Try to load feature names
            try:
                self.feature_names = joblib.load("model_features.pkl")
                print(f"✓ Feature names loaded: {len(self.feature_names)} features")
            except:
                # Use the exact feature names from your training
                self.feature_names = [
                    'Patient ID',
                    'Heart Rate',
                    'Respiratory Rate',
                    'Body Temperature',
                    'Oxygen Saturation',
                    'Systolic Blood Pressure',
                    'Diastolic Blood Pressure',
                    'Age',
                    'Weight (kg)',
                    'Height (m)',
                    'Derived_Pulse_Pressure',
                    'Derived_BMI',
                    'Derived_MAP',
                    'Gender_Male'
                ]
                print(f"✓ Using default feature names from training")
            
            # Try to load preprocessing info
            try:
                with open("preprocessing.json", "r") as f:
                    self.preprocessing_info = json.load(f)
                print("✓ Preprocessing info loaded")
            except:
                self.preprocessing_info = {
                    "gender_mapping": {"Male": 1, "Female": 0},
                    "target_mapping": {"Low Risk": 0, "High Risk": 1}
                }
            
            return True
            
        except Exception as e:
            print(f"✗ Model loading failed: {e}")
            return False
    
    def preprocess_patient_data(self, patient_data):
        """
        Convert patient data to model input format
        MUST match the exact feature names from training
        
        Args:
            patient_data: dict with keys:
                - case_id, age, gender, height, weight
                - vital_signs: {heart_rate, systolic_bp, diastolic_bp, 
                               spo2, respiratory_rate, temperature}
        
        Returns:
            pandas DataFrame ready for model prediction
        """
        try:
            # Extract demographics
            case_id = patient_data.get('case_id', 'UNKNOWN')
            age = float(patient_data.get('age', 0))
            gender = patient_data.get('gender', 'Male')
            height_cm = float(patient_data.get('height', 0))
            weight_kg = float(patient_data.get('weight', 0))
            
            # Convert height from cm to meters
            height_m = height_cm / 100.0
            
            # Encode gender (Male=1, Female=0)
            gender_male = 1 if gender.lower() == 'male' else 0
            
            # Extract vital signs
            vital_signs = patient_data.get('vital_signs', {})
            heart_rate = float(vital_signs.get('heart_rate', 0))
            systolic_bp = float(vital_signs.get('systolic_bp', 0))
            diastolic_bp = float(vital_signs.get('diastolic_bp', 0))
            spo2 = float(vital_signs.get('spo2', 0))
            respiratory_rate = float(vital_signs.get('respiratory_rate', 0))
            body_temperature = float(vital_signs.get('temperature', 0))
            
            # Calculate DERIVED features (as in your training)
            # 1. Pulse Pressure = Systolic - Diastolic
            pulse_pressure = systolic_bp - diastolic_bp
            
            # 2. BMI = weight / (height_m^2)
            bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0
            
            # 3. MAP (Mean Arterial Pressure) = Diastolic + (Pulse Pressure / 3)
            map_value = diastolic_bp + (pulse_pressure / 3)
            
            # Create a simple numeric Patient ID (extract numbers from case_id)
            try:
                patient_id = int(''.join(filter(str.isdigit, case_id)))
            except:
                patient_id = 0
            
            # Create feature dictionary matching EXACT training column names
            features = {
                'Patient ID': patient_id,
                'Heart Rate': heart_rate,
                'Respiratory Rate': respiratory_rate,
                'Body Temperature': body_temperature,
                'Oxygen Saturation': spo2,
                'Systolic Blood Pressure': systolic_bp,
                'Diastolic Blood Pressure': diastolic_bp,
                'Age': age,
                'Weight (kg)': weight_kg,
                'Height (m)': height_m,
                'Derived_Pulse_Pressure': pulse_pressure,
                'Derived_BMI': bmi,
                'Derived_MAP': map_value,
                'Gender_Male': gender_male
            }
            
            # Convert to DataFrame with correct column order
            df = pd.DataFrame([features])
            
            # Ensure column order matches training
            if self.feature_names:
                df = df[self.feature_names]
            
            return df
            
        except Exception as e:
            print(f"Preprocessing error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def predict(self, patient_data):
        """
        Make risk prediction for a patient
        
        Args:
            patient_data: dict with patient information
        
        Returns:
            dict with prediction results
        """
        if not self.model:
            return {
                'error': 'Model not loaded',
                'risk_score': None,
                'condition': 'error',
                'alerts': ['Model not available']
            }
        
        try:
            # Preprocess data
            features_df = self.preprocess_patient_data(patient_data)
            if features_df is None:
                return {
                    'error': 'Data preprocessing failed',
                    'risk_score': None,
                    'condition': 'error',
                    'alerts': ['Invalid input data']
                }
            
            # Debug: Print features
            print("\n--- Features sent to model ---")
            print(features_df.to_string())
            print("------------------------------\n")
            
            # Make prediction
            # predict_proba returns [prob_low_risk, prob_high_risk]
            prediction_proba = self.model.predict_proba(features_df)[0]
            risk_score = float(prediction_proba[1])  # Probability of High Risk
            
            # Get binary prediction
            prediction = self.model.predict(features_df)[0]
            risk_class = "High Risk" if prediction == 1 else "Low Risk"
            
            # Interpret results
            result = self.interpret_prediction(risk_score, risk_class, patient_data)
            
            return result
            
        except Exception as e:
            print(f"Prediction error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': str(e),
                'risk_score': None,
                'condition': 'error',
                'alerts': [f'Prediction failed: {str(e)}']
            }
    
    def interpret_prediction(self, risk_score, risk_class, patient_data):
        """
        Interpret model output and generate clinical alerts
        
        Args:
            risk_score: float probability of high risk (0.0 to 1.0)
            risk_class: str "High Risk" or "Low Risk"
            patient_data: original patient data
        
        Returns:
            dict with interpreted results
        """
        alerts = []
        recommendations = []
        
        # Risk categorization
        if risk_class == "High Risk":
            condition = "HIGH RISK"
            severity = "critical"
            alerts.append("Patient classified as HIGH RISK by AI model")
            recommendations.append("Immediate physician consultation required")
            recommendations.append("Continuous monitoring recommended")
        else:
            if risk_score > 0.3:
                condition = "MODERATE RISK"
                severity = "monitor"
                alerts.append("Patient classified as LOW RISK but close to threshold")
                recommendations.append("Increase monitoring frequency")
            else:
                condition = "LOW RISK"
                severity = "stable"
                recommendations.append("Continue routine monitoring")
        
        # Check vital signs against normal ranges
        vital_signs = patient_data.get('vital_signs', {})
        
        # Heart Rate
        hr = float(vital_signs.get('heart_rate', 0))
        if hr > 0:
            if hr < 60:
                alerts.append("Bradycardia: Heart rate < 60 bpm")
                recommendations.append("Assess for cardiac issues")
            elif hr > 100:
                alerts.append("Tachycardia: Heart rate > 100 bpm")
                recommendations.append("Investigate cause of elevated heart rate")
        
        # Blood Pressure
        systolic = float(vital_signs.get('systolic_bp', 0))
        diastolic = float(vital_signs.get('diastolic_bp', 0))
        if systolic > 0 and diastolic > 0:
            if systolic >= 140 or diastolic >= 90:
                alerts.append("Hypertension detected")
                recommendations.append("Blood pressure management needed")
            elif systolic < 90 or diastolic < 60:
                alerts.append("Hypotension detected")
                recommendations.append("Monitor for signs of shock")
        
        # SpO2
        spo2 = float(vital_signs.get('spo2', 0))
        if spo2 > 0:
            if spo2 < 90:
                alerts.append("CRITICAL: Severe hypoxemia (SpO2 < 90%)")
                recommendations.append("Immediate oxygen therapy required")
                severity = "critical"
            elif spo2 < 95:
                alerts.append("Low oxygen saturation (SpO2 < 95%)")
                recommendations.append("Consider supplemental oxygen")
        
        # Temperature
        temp = float(vital_signs.get('temperature', 0))
        if temp > 0:
            if temp >= 38:
                alerts.append("Fever detected (>=38C)")
                recommendations.append("Monitor temperature regularly")
                recommendations.append("Consider antipyretics if indicated")
            elif temp < 36:
                alerts.append("Hypothermia detected (<36C)")
                recommendations.append("Warming measures required")
        
        # Respiratory Rate
        rr = float(vital_signs.get('respiratory_rate', 0))
        if rr > 0:
            if rr < 12:
                alerts.append("Bradypnea: Respiratory rate < 12")
                recommendations.append("Assess respiratory function")
            elif rr > 20:
                alerts.append("Tachypnea: Respiratory rate > 20")
                recommendations.append("Evaluate for respiratory distress")
        
        # Age-related considerations
        age = float(patient_data.get('age', 0))
        if age > 65 and severity == "critical":
            recommendations.append("Elderly patient: Consider ICU admission")
        
        return {
            'risk_score': round(risk_score, 3),
            'risk_probability_percent': round(risk_score * 100, 1),
            'risk_class': risk_class,
            'condition': condition,
            'severity': severity,
            'alerts': alerts if alerts else ["No critical alerts"],
            'recommendations': recommendations,
            'predicted_at': datetime.now().isoformat(),
            'model_confidence': round(max(risk_score, 1 - risk_score), 3)
        }


# Test function
if __name__ == "__main__":
    print("Testing ML Model Handler...")
    print("="*70)
    
    # Initialize model
    handler = MLModelHandler("risk_classifier_model.pkl")
    
    if not handler.model:
        print("\nERROR: Model not loaded!")
        print("Please ensure risk_classifier_model.pkl is in the current directory")
        exit()
    
    # Test patient data
    test_patient = {
        "case_id": "TEST-001",
        "gender": "Male",
        "age": "45",
        "height": "175",
        "weight": "80",
        "vital_signs": {
            "heart_rate": "85",
            "systolic_bp": "130",
            "diastolic_bp": "85",
            "spo2": "96",
            "respiratory_rate": "16",
            "temperature": "37.2"
        }
    }
    
    print("\nTest Patient Data:")
    print(json.dumps(test_patient, indent=2))
    
    # Get prediction
    print("\nRunning prediction...")
    result = handler.predict(test_patient)
    
    print("\n" + "="*70)
    print("PREDICTION RESULT:")
    print("="*70)
    print(json.dumps(result, indent=2))