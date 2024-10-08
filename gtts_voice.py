import os
import tempfile
from gtts import gTTS
from langdetect import detect
import datetime
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            shift_base = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char  # Non-alphabetic characters remain unchanged
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)
api_key=os.getenv("API_KEY")
api_key=caesar_decrypt(api_key, 3)
class OpenAIClient:
    def __init__(self,prompt):
        openai_api_key = api_key  # Get the API key from the .env file
        self.client = OpenAI(api_key=openai_api_key)
        self.messages=[
                {"role": "system", "content": prompt}
            ]
        

    def speech_to_text_conversion(self, file_path):
        """Converts audio format message to text using OpenAI's Whisper model."""
        with open(file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",  # Model to use for transcription
                file=audio_file  # Audio file to transcribe
            )
        return transcription.text

    def text_chat(self, text):
        """Generate a response using OpenAI based on the context provided."""
        self.messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages)
        bot=response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot})
        return bot

    def text_to_speech_conversion(self, text, slow=False):
        """Converts text to audio format message using gTTS with automatic language detection."""
        if text:
            # Detect the language of the text
            lang = detect(text)

            # Create a temporary audio file
            speech_file_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

            # Convert text to speech using gTTS with the detected language
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(speech_file_path)

            # Read the audio file as binary data
            with open(speech_file_path, "rb") as audio_file:
                audio_data = audio_file.read()

            os.remove(speech_file_path)
            return audio_data
        
        
    
