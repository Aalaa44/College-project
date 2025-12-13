"""
Simulator Bridge - Custom for VitalSignSim TSV Format
Reads vitalsign_output.txt with tab-separated columns:
Time, HR, SpO2, etCO2, RR, NIBP, Rhythm, Event
"""

import os
import time
import threading
from datetime import datetime


class FileBasedSimulatorBridge:
    """
    Monitor VitalSignSim TSV output file
    Format: Time	HR	SpO2	etCO2	RR	NIBP	Rhythm	Event
    """
    
    def __init__(self, file_path='vitalsign_output.txt'):
        """
        Initialize file monitor
        
        Args:
            file_path: Path to vitalsign_output.txt
        """
        self.file_path = file_path
        self.is_running = False
        self.latest_data = {}
        self.callbacks = []
        self.last_size = 0
        self.last_line = ""
        
        print(f"Initializing VitalSignSim file monitor")
        print(f"Monitoring: {os.path.abspath(file_path)}")
    
    def connect(self):
        """Check if file exists and is readable"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    lines = f.readlines()
                
                print(f"✓ File found: {self.file_path}")
                print(f"✓ File contains {len(lines)} lines")
                
                # Parse initial data from last line
                if len(lines) > 1:
                    initial_data = self.parse_tsv_line(lines[-1])
                    if initial_data:
                        self.latest_data = initial_data
                        print(f"✓ Initial data parsed: HR={initial_data.get('heart_rate')}, SpO2={initial_data.get('spo2')}")
                
                self.last_size = os.path.getsize(self.file_path)
                return True
            else:
                print(f"✗ File not found: {self.file_path}")
                print(f"  Expected location: {os.path.abspath(self.file_path)}")
                print(f"  Make sure VitalSignSim is exporting to this file")
                return False
                
        except Exception as e:
            print(f"✗ Error accessing file: {e}")
            return False
    
    def disconnect(self):
        """Stop monitoring"""
        self.is_running = False
        print("✓ File monitoring stopped")
    
    def parse_tsv_line(self, line):
        """
        Parse a single line from the TSV file
        
        Format: Time	HR	SpO2	etCO2	RR	NIBP	Rhythm	Event
        Example: 00:32	98	68	55	37	120/80	Sinus	HR changed
        
        Returns:
            dict with vital signs data or None if parsing fails
        """
        try:
            line = line.strip()
            if not line or line.startswith('Time'):
                return None  # Skip header or empty lines
            
            # Split by tab
            parts = line.split('\t')
            
            if len(parts) < 6:
                return None  # Not enough columns
            
            # Extract values by column index
            time_val = parts[0].strip()
            hr = parts[1].strip()
            spo2 = parts[2].strip()
            etco2 = parts[3].strip()
            rr = parts[4].strip()
            nibp = parts[5].strip()
            rhythm = parts[6].strip() if len(parts) > 6 else "Unknown"
            event = parts[7].strip() if len(parts) > 7 else ""
            
            # Parse blood pressure (format: 120/80)
            systolic = ""
            diastolic = ""
            if '/' in nibp:
                bp_parts = nibp.split('/')
                systolic = bp_parts[0].strip()
                diastolic = bp_parts[1].strip()
            
            # Create data dict
            data = {
                'timestamp': datetime.now().isoformat(),
                'time': time_val,
                'heart_rate': hr,
                'spo2': spo2,
                'etco2': etco2,
                'respiratory_rate': rr,
                'systolic_bp': systolic,
                'diastolic_bp': diastolic,
                'blood_pressure': nibp,
                'rhythm': rhythm,
                'event': event,
                'temperature': '37.0'  # Default, not in file
            }
            
            return data
            
        except Exception as e:
            print(f"Parse error: {e}")
            print(f"Line content: {line[:100]}")
            return None
    
    def get_latest_line(self):
        """Read the most recent line from the file"""
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
            
            # Get last non-empty line that's not the header
            for line in reversed(lines):
                if line.strip() and not line.startswith('Time'):
                    return line
            
            return None
            
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def start_monitoring(self, callback=None):
        """
        Start monitoring the file for changes
        
        Args:
            callback: function(vital_signs) called when new data is added
        """
        if callback:
            self.callbacks.append(callback)
        
        self.is_running = True
        
        def monitor_loop():
            print("✓ File monitoring started")
            print("  Checking for new lines every 500ms...")
            
            while self.is_running:
                try:
                    if not os.path.exists(self.file_path):
                        time.sleep(1)
                        continue
                    
                    # Check if file size changed (new data added)
                    current_size = os.path.getsize(self.file_path)
                    
                    if current_size != self.last_size or current_size > 0:
                        self.last_size = current_size
                        
                        # Get latest line
                        latest_line = self.get_latest_line()
                        
                        if latest_line and latest_line != self.last_line:
                            self.last_line = latest_line
                            
                            # Parse the new line
                            vital_signs = self.parse_tsv_line(latest_line)
                            
                            if vital_signs:
                                self.latest_data = vital_signs
                                
                                # Notify all callbacks
                                for cb in self.callbacks:
                                    try:
                                        cb(vital_signs)
                                    except Exception as e:
                                        print(f"Callback error: {e}")
                    
                    time.sleep(0.5)  # Check every 500ms
                
                except Exception as e:
                    print(f"Monitor error: {e}")
                    time.sleep(1)
        
        # Start monitoring in background thread
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
    
    def get_latest_data(self):
        """Get the most recent vital signs data"""
        return self.latest_data.copy() if self.latest_data else None
    
    def print_status(self):
        """Print current status and latest data"""
        print("\n" + "="*70)
        print("VITALSIGN SIMULATOR - FILE MONITOR STATUS")
        print("="*70)
        print(f"File: {self.file_path}")
        print(f"Running: {self.is_running}")
        print(f"File exists: {os.path.exists(self.file_path)}")
        
        if self.latest_data:
            print("\nLatest Vital Signs:")
            print(f"  Time: {self.latest_data.get('time', 'N/A')}")
            print(f"  Heart Rate: {self.latest_data.get('heart_rate', 'N/A')} bpm")
            print(f"  SpO2: {self.latest_data.get('spo2', 'N/A')}%")
            print(f"  Blood Pressure: {self.latest_data.get('blood_pressure', 'N/A')}")
            print(f"  Respiratory Rate: {self.latest_data.get('respiratory_rate', 'N/A')}")
            print(f"  etCO2: {self.latest_data.get('etco2', 'N/A')}")
            print(f"  Rhythm: {self.latest_data.get('rhythm', 'N/A')}")
            if self.latest_data.get('event'):
                print(f"  Event: {self.latest_data.get('event')}")
        else:
            print("\nNo data available yet")
        print("="*70 + "\n")


# Dummy class for compatibility
class VitalSignsSimulatorBridge:
    """Wrapper for backward compatibility"""
    def __init__(self, *args, **kwargs):
        pass
    
    def connect(self):
        return False
    
    def disconnect(self):
        pass
    
    def start_monitoring(self, callback=None):
        pass
    
    def get_latest_data(self):
        return None


# Test the file monitor
if __name__ == "__main__":
    print("="*70)
    print("VITALSIGN SIMULATOR FILE MONITOR - TEST MODE")
    print("="*70)
    
    # Ask for file path
    file_path = input("\nEnter file path (or press Enter for 'vitalsign_output.txt'): ").strip()
    if not file_path:
        file_path = 'vitalsign_output.txt'
    
    print(f"\nAttempting to connect to: {file_path}")
    
    # Create bridge
    bridge = FileBasedSimulatorBridge(file_path)
    
    # Callback function
    def on_new_data(vital_signs):
        print("\n" + "─"*70)
        print(f"📊 NEW DATA RECEIVED at {vital_signs.get('time', 'N/A')}")
        print("─"*70)
        print(f"   Heart Rate: {vital_signs.get('heart_rate')} bpm")
        print(f"   SpO2: {vital_signs.get('spo2')}%")
        print(f"   Blood Pressure: {vital_signs.get('blood_pressure')} mmHg")
        print(f"   Respiratory Rate: {vital_signs.get('respiratory_rate')}")
        print(f"   etCO2: {vital_signs.get('etco2')}")
        print(f"   Rhythm: {vital_signs.get('rhythm')}")
        if vital_signs.get('event'):
            print(f"   Event: {vital_signs.get('event')}")
        print("─"*70)
    
    # Try to connect
    if bridge.connect():
        print("\n" + "="*70)
        print("✓ CONNECTION SUCCESSFUL!")
        print("="*70)
        
        bridge.start_monitoring(callback=on_new_data)
        
        print("\n📡 Monitoring for changes...")
        print("💡 Tip: Update VitalSignSim to see real-time changes here")
        print("⏹  Press Ctrl+C to stop\n")
        
        try:
            last_print = 0
            while True:
                time.sleep(1)
                
                # Print status every 5 seconds
                current_time = time.time()
                if current_time - last_print >= 5:
                    last_print = current_time
                    latest = bridge.get_latest_data()
                    
                    if latest:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                              f"HR={latest.get('heart_rate')} | "
                              f"SpO2={latest.get('spo2')}% | "
                              f"BP={latest.get('blood_pressure')} | "
                              f"RR={latest.get('respiratory_rate')}")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for data...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("STOPPING MONITOR...")
            print("="*70)
            bridge.disconnect()
            print("✓ Test complete - Bridge disconnected")
    
    else:
        print("\n" + "="*70)
        print("✗ CONNECTION FAILED!")
        print("="*70)
        print("\n🔧 TROUBLESHOOTING:")
        print("  1. Check that VitalSignSim is running")
        print("  2. Verify the file path is correct")
        print("  3. Make sure VitalSignSim is set to export data")
        print("\n📝 Expected file format:")
        print("-" * 70)
        print("Time\tHR\tSpO2\tetCO2\tRR\tNIBP\tRhythm\tEvent")
        print("00:00\t80\t98\t40\t12\t120/80\tSinus\tStart")
        print("00:12\t80\t98\t40\t27\t120/80\tSinus\tRR changed")
        print("-" * 70)
        
        print(f"\n📂 Looking for file at: {os.path.abspath(file_path)}")