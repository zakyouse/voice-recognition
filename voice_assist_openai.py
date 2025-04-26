import os
import sys
import openai
import whisper
from dotenv import load_dotenv
import speech_recognition as sr

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY

r = sr.Recognizer()
# Initialize Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", "large" based on your needs

def listen():
    # Use the microphone to capture audio
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            # Save the audio to a temporary file
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Use OpenAI Whisper to transcribe the audio file
            result = model.transcribe("temp.wav")
            command = result["text"].lower()  # Convert to lowercase
            print("You said:", command)
            os.remove("temp.wav")  # Clean up the temporary file
            return command

        except sr.UnknownValueError:
            print("Sorry, I didn’t catch that.")
            return ""
        except sr.RequestError:
            print("Speech service is down.")
            return ""
        except Exception as e:
            print(f"Error with microphone: {e}")
            return ""

def execute(command):
    if "open firefox" in command:
        os.system("firefox &")
    elif "open upwork" in command:
        os.system("firefox https://www.upwork.com &")
    elif "shutdown" in command:
        os.system("shutdown now")
    elif "exit program" in command:
        print("Exiting program. Bye!")
        sys.exit()
    else:
        print("Command not recognized")

# Main loop
print("Say 'wake up' to start.")
while True:
    command = listen()
    print(command)
    if "wake up" in command:
        print("I'm awake. What should I do?")
        while True:
            command = listen()
            if "goodbye oliver" in command:
                print("Going to sleep. 👋")
                break
            execute(command)
