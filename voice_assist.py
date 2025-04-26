import speech_recognition as sr
import os
import sys

r = sr.Recognizer()

def listen():
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            command = r.recognize_google(audio)
            command = command.lower()
            print("You said:", command)
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
