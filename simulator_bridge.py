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
        
        print(f"Initializing VitalSignSim file monitor")
        print(f"Monitoring: {os.path.abspath(file_path)}")
    
    def connect(self):
        """Check if file exists and is readable"""
        try:
            if not os.path.exists(self.file_path):
                print(f"✗ File not found: {self.file_path}")
                print(f"  Expected location: {os.path.abspath(self.file_path)}")
                print(f"  Make sure VitalSignSim is exporting to this file")
                return False
            
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
            
            print(f"✓ File found: {self.file_path}")
            print(f"✓ File contains {len(lines)} lines")
            return True
                
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
                return None
            
            parts = line.split('\t')
            
            if len(parts) < 6:
                return None
            
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
            systolic, diastolic = "", ""
            if '/' in nibp:
                bp_parts = nibp.split('/')
                systolic = bp_parts[0].strip()
                diastolic = bp_parts[1].strip()
            
            return {
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
                'temperature': '37.0'
            }
            
        except Exception as e:
            print(f"Parse error: {e}")
            print(f"Line content: {line[:100]}")
            return None
    
    def parse_time_to_seconds(self, time_str):
        """
        Convert time string (MM:SS or HH:MM:SS) to total seconds
        
        Args:
            time_str: Time string like "00:32" or "01:15:30"
        
        Returns:
            int: Total seconds
        """
        try:
            parts = time_str.split(':')
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            else:
                return 0
        except:
            return 0
    
    def start_monitoring(self, callback=None):
        """
        Start iterating through the file rows sequentially with realistic timing
        """
        if callback:
            self.callbacks.append(callback)
        
        self.is_running = True
        
        def monitor_loop():
            print("✓ Starting sequential data playback...")
            
            try:
                if not os.path.exists(self.file_path):
                    print("✗ File not found.")
                    return

                with open(self.file_path, 'r') as f:
                    lines = f.readlines()

                # Filter out headers and empty lines
                data_rows = [line for line in lines 
                           if line.strip() and not line.startswith('Time')]
                print(f"✓ Loaded {len(data_rows)} rows of data.")

                # Track previous timestamp
                prev_time_seconds = None

                # Iterate through rows
                for line in data_rows:
                    if not self.is_running:
                        break
                    
                    vital_signs = self.parse_tsv_line(line)
                    
                    if vital_signs:
                        self.latest_data = vital_signs
                        
                        # Send to callbacks
                        for cb in self.callbacks:
                            try:
                                cb(vital_signs)
                            except Exception as e:
                                print(f"Callback error: {e}")
                        
                        # Calculate delay based on timestamp difference
                        current_time_seconds = self.parse_time_to_seconds(vital_signs['time'])
                        
                        if prev_time_seconds is not None:
                            time_diff = current_time_seconds - prev_time_seconds
                            # Use time difference if positive, otherwise default to 1 second
                            delay = time_diff if time_diff > 0 else 1.0
                        else:
                            # First row, use default delay
                            delay = 1.0
                        
                        prev_time_seconds = current_time_seconds
                        time.sleep(delay)
                    else:
                        # If parsing failed, use default delay
                        time.sleep(1.0)
                
                print("✓ End of data file reached.")
                self.is_running = False

            except Exception as e:
                print(f"Playback error: {e}")
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
    
    def get_latest_data(self):
        """Get the most recent vital signs data"""
        return self.latest_data.copy() if self.latest_data else None