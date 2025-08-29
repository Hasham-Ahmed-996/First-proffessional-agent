import openai
import json
from typing import Dict, Any, Optional
from config import OPENAI_API_KEY, OPENAI_MODEL, DOCTORS

class ChatGPTHandler:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise EnvironmentError("OPENAI_API_KEY not found in config. Please set your OpenAI API key.")
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        """Create the system prompt with doctor information"""
        doctors_info = []
        for doc_id, info in DOCTORS.items():
            doctors_info.append(
                f"{info['name']} ({info['specialty']}): {', '.join(info['days'])} {info['hours'][0]}:00-{info['hours'][1]}:00"
            )
        return (
            "You are a helpful medical appointment scheduler. "
            "Here are the available doctors and their schedules:\n" +
            "\n".join(doctors_info)
        )

    def get_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        # Limit conversation history to last 10 messages
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in self.conversation_history:
            messages.append(msg)
        messages.append({"role": "user", "content": user_input})
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Sorry, there was an error communicating with ChatGPT: {e}"

    def extract_appointment_info(self, user_input: str) -> Dict[str, Any]:
        # Use GPT to extract structured info
        try:
            prompt = (
                f"{self.system_prompt}\n"
                "Extract the following information from the user's message if available: "
                "patient_name, doctor_preference, day_preference, time_preference. "
                "Return as a JSON object."
            )
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            import json
            import re
            match = re.search(r"\{.*\}", response.choices[0].message.content, re.DOTALL)
            if match:
                info = json.loads(match.group())
                # Validate doctor name
                if info.get("doctor_preference") and info["doctor_preference"].lower() not in DOCTORS:
                    info["doctor_preference"] = None
                return info
            return {}
        except Exception as e:
            return {}

    def reset_conversation(self):
        self.conversation_history = []