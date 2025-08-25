import pyttsx3
import speech_recognition as sr
import datetime
 
# Initialize recognizer
recognizer = sr.Recognizer()
 
# Speak function
def speak_text(text):
    print("Agent:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
 
# Listen function
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio).lower()
            print("You said:", response)
            return response
        except sr.UnknownValueError:
            speak_text("Sorry, I did not catch that.")
            return None
        except sr.RequestError:
            speak_text("Sorry, my speech service is unavailable.")
            return None
 
# Doctor schedules (20-minute slots, alternating hours)
doctors = {
    "ali": {"days": ["monday", "wednesday", "friday"], "hours": (9, 17)},
    "sara": {"days": ["tuesday", "thursday"], "hours": (10, 18)},
    "john": {"days": ["saturday","sunday"], "hours": (9, 13)}
}
 
# Generate slots in 20 min intervals
def generate_slots(start_hour, end_hour):
    slots = []
    start = datetime.datetime(2025, 1, 1, start_hour, 0)
    end = datetime.datetime(2025, 1, 1, end_hour, 0)
    while start < end:
        slots.append(start.strftime("%I:%M %p"))
        start += datetime.timedelta(minutes=20)
    return slots
 
# Try to normalize spoken time into a slot format
def normalize_time(slot):
    if not slot:
        return None
    slot = slot.upper().replace(".", "").strip()
    formats = ["%I:%M %p", "%I %p"]  # Accept "10:00 AM" or "10 AM"
    for fmt in formats:
        try:
            return datetime.datetime.strptime(slot, fmt).strftime("%I:%M %p")
        except ValueError:
            continue
    return None
 
# Main agent logic
def appointment_scheduler():
    speak_text("Welcome to the voice appointment scheduler.")
 
    # --- Ask for patient name ---
    patient_name = None
    while not patient_name:
        speak_text("Please tell me your name, or say exit to quit.")
        name = listen()
        if name == "exit":
            speak_text("Goodbye!")
            return
        if name:
            patient_name = name
 
    # --- Tell available doctors and their days ---
    availability_message = "Here are the available doctors and their working days: "
    for doc, info in doctors.items():
        days_list = ", ".join(info["days"])
        availability_message += f"Dr. {doc.title()} works on {days_list}. "
    speak_text(availability_message)
 
    # --- Ask for doctor ---
    doctor_name = None
    while not doctor_name:
        speak_text("which doctor do you want to book? Ali, Sara, or John?")
        doc = listen()
        if doc == "exit":
            speak_text("Goodbye!")
            return
        if doc in doctors:
            doctor_name = doc
        else:
            speak_text("Sorry, I could not detect the doctor. Please try again.")
 
    # --- Ask for day (only from doctor's available days) ---
    chosen_day = None
    while not chosen_day:
        speak_text(f"Dr. {doctor_name.title()} is available on {', '.join(doctors[doctor_name]['days'])}. Which day should I book your appointment on?")
        day = listen()
        if day == "exit":
            speak_text("Goodbye!")
            return
        if day and day in doctors[doctor_name]["days"]:
            chosen_day = day
        else:
            speak_text(f"Dr. {doctor_name.title()} does not work on that day. Please try again.")
 
    # --- Ask for time slot ---
    slots = generate_slots(*doctors[doctor_name]["hours"])
    chosen_slot = None
    while not chosen_slot:
        speak_text(f"Available slots for Dr. {doctor_name.title()} on {chosen_day} are: {', '.join(slots[:5])} ... and more.")
        speak_text("Please say your preferred time, like 10:00 AM.")
        slot = listen()
        if slot == "exit":
            speak_text("Goodbye!")
            return
        user_time = normalize_time(slot)
        if user_time and user_time in slots:
            chosen_slot = user_time
        else:
            speak_text("Sorry, that time is not available. Please try again.")
 
    # --- Confirm booking ---
    speak_text(f"Booking confirmed for {patient_name} with Dr. {doctor_name.title()} on {chosen_day.title()} at {chosen_slot}.")
    speak_text("Goodbye!")
 
# Run the agent
if __name__ == "__main__":
    appointment_scheduler()