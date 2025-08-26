import datetime
from typing import List, Dict, Any, Optional
from config import DOCTORS

class AppointmentManager:
    def __init__(self):
        self.appointments = []  # In a real app, this would be a database
        
    def generate_time_slots(self, doctor_id: str, day: str) -> List[str]:
        """Generate available time slots for a doctor on a specific day"""
        if doctor_id not in DOCTORS:
            return []
            
        doctor = DOCTORS[doctor_id]
        if day.lower() not in doctor["days"]:
            return []
            
        slots = []
        start_hour, end_hour = doctor["hours"]
        
        # Create datetime object for the day
        start_time = datetime.datetime(2025, 1, 1, start_hour, 0)
        end_time = datetime.datetime(2025, 1, 1, end_hour, 0)
        
        current_time = start_time
        while current_time < end_time:
            slot_str = current_time.strftime("%I:%M %p")
            
            # Check if slot is already booked
            if not self.is_slot_booked(doctor_id, day, slot_str):
                slots.append(slot_str)
                
            current_time += datetime.timedelta(minutes=20)
            
        return slots
    
    def is_slot_booked(self, doctor_id: str, day: str, time_slot: str) -> bool:
        """Check if a specific slot is already booked"""
        for appointment in self.appointments:
            if (appointment["doctor_id"] == doctor_id and 
                appointment["day"].lower() == day.lower() and 
                appointment["time_slot"] == time_slot):
                return True
        return False
    
    def book_appointment(self, patient_name: str, doctor_id: str, day: str, time_slot: str) -> bool:
        """Book an appointment"""
        if self.is_slot_booked(doctor_id, day, time_slot):
            return False
            
        appointment = {
            "patient_name": patient_name,
            "doctor_id": doctor_id,
            "doctor_name": DOCTORS[doctor_id]["name"],
            "day": day,
            "time_slot": time_slot,
            "booking_time": datetime.datetime.now().isoformat()
        }
        
        self.appointments.append(appointment)
        return True
    
    def get_doctor_availability_summary(self) -> str:
        """Get a summary of all doctors and their availability"""
        summary = []
        for doc_id, info in DOCTORS.items():
            days = ", ".join([day.title() for day in info["days"]])
            summary.append(f"{info['name']} ({info['specialty']}) - Available: {days}")
        return "\n".join(summary)
    
    def normalize_time_input(self, time_input: str) -> Optional[str]:
        """Normalize various time inputs to standard format"""
        if not time_input:
            return None
            
        time_input = time_input.upper().replace(".", "").strip()
        
        # Common time formats to try
        formats = [
            "%I:%M %p",  # 10:00 AM
            "%I %p",     # 10 AM
            "%H:%M",     # 14:00
            "%H"         # 14
        ]
        
        for fmt in formats:
            try:
                parsed_time = datetime.datetime.strptime(time_input, fmt)
                return parsed_time.strftime("%I:%M %p")
            except ValueError:
                continue
                
        return None