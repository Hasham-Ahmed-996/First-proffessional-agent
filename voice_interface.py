import pyttsx3
import speech_recognition as sr
from typing import Optional

class VoiceInterface:
    def __init__(self, rate: int = 150, volume: float = 0.9):
        self.recognizer = sr.Recognizer()
        self.rate = rate
        self.volume = volume
        
    def speak(self, text: str) -> None:
        """Convert text to speech"""
        print(f"Assistant: {text}")
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            response = self.recognizer.recognize_google(audio).lower().strip()
            print(f"You said: {response}")
            return response
            
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand what you said. Please try again.")
            return None
        except sr.RequestError as e:
            self.speak("Sorry, there's an issue with the speech recognition service.")
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in listen(): {e}")
            return None