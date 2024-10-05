import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import musiclibrary

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    command = command.lower()
    print(f"Processing command: {command}")  # Debugging print

    # Open websites
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
    elif command.startswith("play"):
        song=command.split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)

        

    # Open Instagram app (using correct identifier from AppsFolder)
    elif "open instagram" in command:
        speak("Opening Instagram")
        os.system("start shell:AppsFolder\\Facebook.InstagramBeta_8xx8rvfyw5nnt!App")
    # Open Whatsapp app (using correct identifier from AppsFolder)
    elif "open whatsapp" in command:
        speak("Opening Whatsapp")
        os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")

    # Open installed applications (Windows examples)
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.startfile("notepad.exe")
    elif "open calculator" in command:
        speak("Opening Calculator")
        os.startfile("calc.exe")
    # elif "open whatsapp" in command:
    #     speak("Opening WhatsApp")
    #     try:
    #         # Full path to WhatsApp executable
    #         path_to_whatsapp = "C:/Path/To/WhatsApp.exe"
    #         os.startfile(path_to_whatsapp)
    #     except FileNotFoundError:
    #         speak("WhatsApp is not installed or path is incorrect.")
    #     # Alternative for Microsoft Store version
    #     os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")

    # Close calculator
    elif "close calculator" in command:
        speak("Closing Calculator")
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
    speak("Initializing Abdullah...")

    while True:
        try:
            # Use the microphone for input
            with sr.Microphone() as source:
                print("Listening for 'abdullah'...")
                # Reduced time for ambient noise adjustment
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Capture the audio with increased timeout and phrase limit
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)

                # Convert speech to text
                word = recognizer.recognize_google(audio)
                print(f"You said: {word}")

                # Respond to the keyword "abdullah"
                if word.lower() == "abdullah":
                    speak("Yes, how can I help?")

                    # Listen for the command with adjusted timeout
                    with sr.Microphone() as source:
                        print("Abdullah active, listening for command...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)

                        # Convert speech to text
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")  # Debugging print

                        # Process the command
                        process_command(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from the Google Speech Recognition service; {e}")
