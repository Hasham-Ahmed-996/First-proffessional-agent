import sys
import os
from typing import Dict, Any, Optional
from voice_interface import VoiceInterface
from chatgpt_handler import ChatGPTHandler
from appointment_manager import AppointmentManager
from config import DOCTORS

# Handle frozen executable paths
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)

class SmartAppointmentScheduler:
    def __init__(self):
        self.voice = VoiceInterface()
        self.chatgpt = ChatGPTHandler()
        self.appointment_manager = AppointmentManager()
        self.booking_context = {}
        
    def run(self):
        """Main application loop"""
        try:
            self.voice.speak("Hello! I'm your AI appointment scheduling assistant. How can I help you today?")
            
            while True:
                user_input = self.voice.listen()
                
                if not user_input:
                    continue
                    
                # Check for exit commands
                if any(word in user_input for word in ["exit", "quit", "goodbye", "bye"]):
                    self.voice.speak("Thank you for using our appointment system. Have a great day!")
                    break
                
                # Process the user input with ChatGPT
                response = self.process_user_input(user_input)
                self.voice.speak(response)
                
        except KeyboardInterrupt:
            self.voice.speak("Goodbye!")
        except Exception as e:
            print(f"Application error: {e}")
            self.voice.speak("I'm sorry, there was an unexpected error. Please try again later.")
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return appropriate response"""
        # Extract appointment information
        extracted_info = self.chatgpt.extract_appointment_info(user_input)
        
        # Update booking context with extracted information
        self.update_booking_context(extracted_info)
        
        # Check if we have enough information to book
        if self.is_booking_complete():
            return self.attempt_booking()
        
        # Get conversational response from ChatGPT
        context_info = {
            "current_booking": self.booking_context,
            "available_doctors": list(DOCTORS.keys()),
            "doctor_schedules": {doc_id: info["days"] for doc_id, info in DOCTORS.items()}
        }
        
        response = self.chatgpt.get_response(user_input, context_info)
        
        # Add helpful information based on what's missing
        if not self.booking_context.get("patient_name"):
            if "name" not in response.lower():
                response += " Could you please tell me your name?"
        elif not self.booking_context.get("doctor_preference"):
            if "doctor" not in response.lower():
                response += f" We have {', '.join([info['name'] for info in DOCTORS.values()])} available."
        elif not self.booking_context.get("day_preference"):
            doctor_id = self.booking_context.get("doctor_preference")
            if doctor_id and doctor_id in DOCTORS:
                days = ", ".join(DOCTORS[doctor_id]["days"])
                response += f" {DOCTORS[doctor_id]['name']} is available on {days}."
        
        return response
    
    def update_booking_context(self, extracted_info: Dict[str, Any]):
        """Update the booking context with new information"""
        for key, value in extracted_info.items():
            if value and value != "null":
                if key == "doctor_preference":
                    # Normalize doctor names
                    value = value.lower()
                    if value in DOCTORS:
                        self.booking_context[key] = value
                elif key == "day_preference":
                    # Normalize day names
                    value = value.lower()
                    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    if value in days:
                        self.booking_context[key] = value
                else:
                    self.booking_context[key] = value
    
    def is_booking_complete(self) -> bool:
        """Check if we have all required information for booking"""
        required_fields = ["patient_name", "doctor_preference", "day_preference", "time_preference"]
        return all(field in self.booking_context and self.booking_context[field] for field in required_fields)
    
    def attempt_booking(self) -> str:
        """Attempt to book the appointment with current context"""
        patient_name = self.booking_context["patient_name"]
        doctor_id = self.booking_context["doctor_preference"]
        day = self.booking_context["day_preference"]
        time_input = self.booking_context["time_preference"]
        
        # Normalize the time
        normalized_time = self.appointment_manager.normalize_time_input(time_input)
        
        if not normalized_time:
            return f"I couldn't understand the time '{time_input}'. Could you please specify a time like '10:00 AM' or '2:30 PM'?"
        
        # Check if the doctor works on that day
        if day not in DOCTORS[doctor_id]["days"]:
            available_days = ", ".join(DOCTORS[doctor_id]["days"])
            return f"I'm sorry, {DOCTORS[doctor_id]['name']} doesn't work on {day.title()}. They're available on {available_days}."
        
        # Get available slots
        available_slots = self.appointment_manager.generate_time_slots(doctor_id, day)
        
        if normalized_time not in available_slots:
            if available_slots:
                slots_str = ", ".join(available_slots[:5])
                return f"I'm sorry, {normalized_time} is not available. Here are some available times: {slots_str}. Would you like one of these instead?"
            else:
                return f"I'm sorry, {DOCTORS[doctor_id]['name']} has no available slots on {day.title()}."
        
        # Book the appointment
        success = self.appointment_manager.book_appointment(patient_name, doctor_id, day, normalized_time)
        
        if success:
            doctor_name = DOCTORS[doctor_id]["name"]
            confirmation = f"Perfect! I've booked your appointment with {doctor_name} on {day.title()} at {normalized_time}. "
            confirmation += f"Please arrive 15 minutes early. Is there anything else I can help you with?"
            
            # Reset booking context for next appointment
            self.booking_context = {}
            return confirmation
        else:
            return "I'm sorry, there was an issue booking your appointment. Please try again."

if __name__ == "__main__":
    try:
        scheduler = SmartAppointmentScheduler()
        scheduler.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        print("Make sure you have set your OpenAI API key in the .env file")