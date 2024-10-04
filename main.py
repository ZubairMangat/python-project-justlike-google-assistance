import speech_recognition as sr
import pyttsx3
import webbrowser
import os

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    command = command.lower()
    print(f"Processing command: {command}")  # Debugging print
    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    # Open installed applications (Windows examples)
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.startfile("notepad.exe")
    elif "open calculator" in command:
        speak("Opening Calculator")
        os.startfile("calc.exe")

    # Close calculator
    elif "close calculator" in command:
        speak("Closing Calculator")
        # First, check if calc.exe is running
        is_running = os.system("tasklist | findstr /i calc.exe") == 0
        if is_running:
            os.system("taskkill /f /im calc.exe")
            speak("Calculator closed.")
        else:
            speak("Calculator is not running.")

    # If no predefined command matches, perform a Google search
    else:
        speak(f"Searching for {command} on Google")
        query = command.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        print(f"Google search for: {command}")

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            # Use the microphone for input
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                # Adjust for ambient noise for better accuracy
                recognizer.adjust_for_ambient_noise(source)
                # Capture the audio
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

                # Convert speech to text
                word = recognizer.recognize_google(audio)
                print(f"You said: {word}")

                # Respond to the keyword "Jarvis"
                if word.lower() == "jarvis":
                    speak("Yes, how can I help?")
                    # listen for the command
                    with sr.Microphone() as source:
                        print("Jarvis active, listening for command...")
                        # Adjust for ambient noise
                        recognizer.adjust_for_ambient_noise(source)
                        # Capture the audio (increase timeout and phrase time limit for commands)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                        # Convert speech to text
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")  # Debugging print

                        # Process the command
                        process_command(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results from the Google Speech Recognition service.")
