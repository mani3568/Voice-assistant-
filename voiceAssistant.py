import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import wikipedia
import random
import smtplib
import time
from tkinter import *
from PIL import Image, ImageTk

# Initialize pyttsx3 for text-to-speech
voiceEngine = pyttsx3.init('sapi5')
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[1].id)

def speak(text):
    """Convert text to speech."""
    voiceEngine.say(text)
    voiceEngine.runAndWait()

def wish():
    """Wish the user based on time of day."""
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Voice Assistant. How can I assist you today?")

def takeCommand():
    """Take voice input from the user and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        status_text.set("Listening...")
        window.update()
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
        status_text.set(f"You said: {command}")
        window.update()
    except Exception as e:
        print("Sorry, I didn't catch that. Could you say it again?")
        status_text.set("Sorry, I didn't catch that. Could you say it again?")
        window.update()
        return "None"
    
    return command.lower()

def executeCommand(command):
    """Execute tasks based on the user's voice command."""
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("youtube.com")

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("google.com")

    elif 'play music' in command:
        music_dir = 'C:\\Users\\Public\\Music'
        songs = os.listdir(music_dir)
        speak("Playing music")
        random_song = os.path.join(music_dir, random.choice(songs))
        os.startfile(random_song)

    elif 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'send email' in command:
        try:
            speak("Whom should I send the email to?")
            to = input("Enter recipient's email: ")  # Could replace with voice command input
            speak("What should the email say?")
            content = takeCommand()
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry, I wasn't able to send the email.")

    else:
        speak("Sorry, I am not able to understand the command.")

def startListening():
    """Start listening for user commands."""
    command = takeCommand()
    if command != "None":
        executeCommand(command)

def sendEmail(to, content):
    """Send an email."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')  # Use app-specific password
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

# GUI Window Setup
window = Tk()
window.title("Voice Assistant")
window.geometry('400x400')
window.config(bg='LightBlue1')

status_text = StringVar()
status_text.set("Press the microphone to start...")

Label(window, text='Voice Assistant', bg='LightBlue1', fg='black', font=('Courier', 15)).pack(pady=20)

# Display microphone image as a button
mic_image = Image.open("mic.jpg")  # Add the path to your microphone icon
mic_image = mic_image.resize((100, 100), Image.Resampling.LANCZOS)
mic_photo = ImageTk.PhotoImage(mic_image)

mic_button = Button(window, image=mic_photo, command=startListening)
mic_button.pack(pady=50)

# Display status label
Label(window, textvariable=status_text, bg='LightBlue1', fg='black', font=('Courier', 12)).pack(pady=20)

# Wish the user on startup
wish()

# Run the window loop
window.mainloop()
