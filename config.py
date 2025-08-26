import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# Doctor schedules (20-minute slots)
DOCTORS = {
    "ali": {
        "name": "Dr. Ali",
        "specialty": "General Medicine",
        "days": ["monday", "wednesday", "friday"], 
        "hours": (9, 17)
    },
    "sara": {
        "name": "Dr. Sara",
        "specialty": "Pediatrics",
        "days": ["tuesday", "thursday"], 
        "hours": (10, 18)
    },
    "john": {
        "name": "Dr. John",
        "specialty": "Cardiology",
        "days": ["saturday", "sunday"], 
        "hours": (9, 13)
    }
}

# Voice settings
VOICE_RATE = 150
VOICE_VOLUME = 0.9