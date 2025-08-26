# Smart Voice Appointment Scheduler with ChatGPT Integration

An intelligent voice-based appointment scheduling system that uses ChatGPT 4o Mini for natural language understanding and conversation.

## Features

- **Natural Language Processing**: Powered by ChatGPT 4o Mini for intelligent conversation
- **Voice Interface**: Complete voice interaction using speech recognition and text-to-speech
- **Smart Information Extraction**: Automatically extracts appointment details from natural speech
- **Flexible Input**: Understands various ways of expressing dates and times
- **Context Awareness**: Maintains conversation context throughout the booking process
- **Doctor Management**: Supports multiple doctors with different schedules and specialties

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

3. **Run the Application**:
   ```bash
   python smart_scheduler.py
   ```

## Usage Examples

The system understands natural language inputs like:

- "Hi, I'm John Smith and I'd like to book an appointment with Dr. Ali for Monday morning"
- "Can I see Dr. Sara next Tuesday around 2 PM?"
- "I need to schedule with the cardiologist for this weekend"
- "Book me with Ali on Friday at 10 AM"

## Available Doctors

- **Dr. Ali** (General Medicine): Monday, Wednesday, Friday (9 AM - 5 PM)
- **Dr. Sara** (Pediatrics): Tuesday, Thursday (10 AM - 6 PM)  
- **Dr. John** (Cardiology): Saturday, Sunday (9 AM - 1 PM)

## Voice Commands

- Say "exit", "quit", "goodbye", or "bye" to end the session
- The system will guide you through the booking process conversationally

## Technical Architecture

- `smart_scheduler.py`: Main application orchestrator
- `voice_interface.py`: Handles speech recognition and text-to-speech
- `chatgpt_handler.py`: Manages ChatGPT API interactions
- `appointment_manager.py`: Handles appointment logic and scheduling
- `config.py`: Configuration and doctor schedules

## Requirements

- Python 3.7+
- OpenAI API key
- Microphone for voice input
- Speakers for voice output