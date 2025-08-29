from typing import List, Dict, Any, Optional
from config import DOCTORS
import datetime
import logging

logging.basicConfig(level=logging.INFO)

class AppointmentManager:
    def __init__(self):
        self.appointments = []  # In-memory list

    def generate_time_slots(self, doctor_id: str, day: str) -> List[str]:
        """Generate available time slots for a doctor on a specific day"""
        if doctor_id not in DOCTORS:
            logging.error(f"Doctor ID '{doctor_id}' not found.")
            return []
        doctor = DOCTORS[doctor_id]
        if day.lower() not in doctor["days"]:
            logging.error(f"Day '{day}' not available for doctor '{doctor_id}'.")
            return []
        slots = []
        start_hour, end_hour = doctor["hours"]
        start_time = datetime.datetime(2025, 1, 1, start_hour, 0)
        end_time = datetime.datetime(2025, 1, 1, end_hour, 0)
        current_time = start_time
        while current_time < end_time:
            slot = current_time.strftime("%H:%M")
            if not self.is_slot_booked(doctor_id, day, slot):
                slots.append(slot)
            current_time += datetime.timedelta(minutes=20)
        return slots

    def is_slot_booked(self, doctor_id: str, day: str, time_slot: str) -> bool:
        """Check if a specific slot is already booked"""
        for appointment in self.appointments:
            if (appointment["doctor_id"] == doctor_id and
                appointment["day"] == day and
                appointment["time_slot"] == time_slot):
                return True
        return False

    def book_appointment(self, patient_name: str, doctor_id: str, day: str, time_slot: str) -> bool:
        """Book an appointment"""
        if self.is_slot_booked(doctor_id, day, time_slot):
            logging.warning(f"Slot {time_slot} on {day} for doctor {doctor_id} is already booked.")
            return False
        self.appointments.append({
            "patient_name": patient_name,
            "doctor_id": doctor_id,
            "day": day,
            "time_slot": time_slot
        })
        logging.info(f"Booked appointment for {patient_name} with {doctor_id} on {day} at {time_slot}.")
        return True

    def get_doctor_availability_summary(self) -> str:
        summary = []
        for doc_id, info in DOCTORS.items():
            days = ", ".join(info["days"])
            summary.append(f"{info['name']} ({info['specialty']}): {days} {info['hours'][0]}:00-{info['hours'][1]}:00")
        return "\n".join(summary)

    def normalize_time_input(self, time_input: str) -> Optional[str]:
        """Normalize various time input formats to HH:MM"""
        try:
            time_obj = datetime.datetime.strptime(time_input, "%H:%M")
            return time_obj.strftime("%H:%M")
        except ValueError:
            try:
                time_obj = datetime.datetime.strptime(time_input, "%I:%M %p")
                return time_obj.strftime("%H:%M")
            except ValueError:
                logging.error(f"Invalid time format: {time_input}")
                return None