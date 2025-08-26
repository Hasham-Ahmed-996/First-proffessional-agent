import openai
import json
from typing import Dict, Any, Optional
from config import OPENAI_API_KEY, OPENAI_MODEL, DOCTORS

class ChatGPTHandler:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file")
        
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.conversation_history = []
        self.system_prompt = self._create_system_prompt()
        
    def _create_system_prompt(self) -> str:
        """Create the system prompt with doctor information"""
        doctors_info = []
        for doc_id, info in DOCTORS.items():
            doctors_info.append(
                f"- {info['name']} ({info['specialty']}): Available {', '.join(info['days'])} "
                f"from {info['hours'][0]}:00 to {info['hours'][1]}:00"
            )
        
        return f"""You are a helpful medical appointment scheduling assistant. Your job is to help patients book appointments with doctors.

Available doctors and their schedules:
{chr(10).join(doctors_info)}

Guidelines:
1. Be friendly, professional, and empathetic
2. Extract key information: patient name, preferred doctor, day, and time
3. If information is missing or unclear, ask clarifying questions
4. Suggest alternatives if requested slots aren't available
5. Confirm all details before finalizing appointments
6. Handle natural language inputs like "next Tuesday", "morning", "afternoon"
7. Be understanding if patients need to reschedule or have concerns

Always respond in a conversational, helpful manner. Keep responses concise but warm.
"""

    def get_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Get ChatGPT response for user input"""
        try:
            # Add context information if provided
            if context:
                context_str = f"Current booking context: {json.dumps(context, indent=2)}"
                user_message = f"{context_str}\n\nUser said: {user_input}"
            else:
                user_message = user_input
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Get response from ChatGPT
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history[-10:],  # Keep last 10 messages for context
                max_tokens=200,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content.strip()
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            print(f"ChatGPT API error: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Could you please try again?"
    
    def extract_appointment_info(self, user_input: str) -> Dict[str, Any]:
        """Extract structured appointment information from user input"""
        try:
            extraction_prompt = f"""
Extract appointment information from this user input: "{user_input}"

Return a JSON object with these fields (use null if not mentioned):
- patient_name: string
- doctor_preference: string (ali, sara, john, or null)
- day_preference: string (monday, tuesday, etc., or null)
- time_preference: string (any time mentioned, or null)
- special_requests: string (any additional notes)

Available doctors: Ali (General Medicine), Sara (Pediatrics), John (Cardiology)

Example: {{"patient_name": "John Smith", "doctor_preference": "ali", "day_preference": "monday", "time_preference": "10 AM", "special_requests": null}}
"""
            
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": extraction_prompt}],
                max_tokens=150,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # If JSON parsing fails, return empty dict
                return {}
                
        except Exception as e:
            print(f"Information extraction error: {e}")
            return {}
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []