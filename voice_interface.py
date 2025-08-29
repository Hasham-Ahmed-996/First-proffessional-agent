import openai
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in .env file. Please set your OpenAI API key.")

openai.api_key = api_key

class VoiceInterface:
    def __init__(self):
        pass  # No need for recognizer or pyttsx3

    def speak(self, text: str) -> None:
        """Convert text to speech using OpenAI TTS"""
        print(f"Assistant: {text}")
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice="alloy",  # You can choose other voices: echo, fable, etc.
                input=text
            )
            # Save the audio to a file and play it
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            # Play the audio (Windows)
            os.system("start output.mp3")
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self, timeout: int = 10) -> Optional[str]:
        """Listen for voice input and convert to text using OpenAI Whisper"""
        try:
            import sounddevice as sd
            import numpy as np
            import scipy.io.wavfile as wav

            print("Listening...")
            fs = 16000  # Whisper expects 16kHz
            duration = timeout
            print("Please speak now...")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()
            wav.write("input.wav", fs, recording)

            # Send audio to OpenAI Whisper
            with open("input.wav", "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            response = transcript.text.lower().strip()
            print(f"You said: {response}")
            return response

        except Exception as e:
            print(f"Speech recognition error: {e}")
            self.speak("Sorry, I couldn't understand what you said. Please try again.")
            return None