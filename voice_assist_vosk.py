import os
import sys
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# Load Vosk model (make sure you download one if not yet)
model = Model("model")  # Folder where your model is

# Audio settings
samplerate = 44100 
device = 1  

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen():
    print("Listening...")
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                               dtype='int16', channels=1, callback=callback):
            rec = KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    command = result.get("text", "").lower()
                    if command:
                        print("You said:", command)
                        return command
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
