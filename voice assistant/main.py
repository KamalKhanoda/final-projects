import speech_recognition as sr
import pyttsx3
from pytube import Search
import webbrowser
from bs4 import BeautifulSoup as bs
import requests
import os

def playYoutubeVideo(query):
    try:
        s = Search(query)
        videoUrl = s.results[0].watch_url
        webbrowser.open(videoUrl)
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        speak(f"Error searching YouTube: {e}")
    
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Listen for up to 30 seconds, stop after 10 seconds of silence
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=20)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return ""
    

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the results for {query}")
ls = ["notepad", "calculator", "paint"]
def open_app(app_name):
    app_name = app_name.lower()
    if "notepad" in app_name:
        os.system("start notepad")
        speak("Opening Notepad.")
    elif "calculator" in app_name:
        os.system("start calc")
        speak("Opening Calculator.")
    elif "paint" in app_name:
        os.system("start mspaint")
        speak("Opening Paint.")
    else:
        speak("Sorry, I can't open that application.")

def main():
    while True:
        command = listen()
        if not command:
            continue

        if "hello" in command:
            speak("Yes,sir!")

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        elif "search" in command and "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            if query:
                google_search(query)
            else:
                speak("Please specify what you want to search for.")

        elif "play" in command or "youtube" in command:
            query = command.replace("play", "").replace("youtube", "").strip()
            if query:
                speak(f"Playing the first YouTube video for '{query}'...")
                playYoutubeVideo(query)
            else:
                speak("Please provide a search term for the video.")

        elif "open" in command:
            app_name = command.replace("open", "").strip()
            # Check if it's an app
            if any(app in app_name for app in ls):
                open_app(app_name)
            # Otherwise, treat as website
            elif app_name:
                site = app_name
                if not site.startswith("http"):
                    site = site.replace(" ", "")
                    url = f"https://{site}.com"
                else:
                    url = site
                webbrowser.open(url)
                speak(f"Opening {url}")
            else:
                speak("Please specify what you want to open.")

        elif "open website" in command or "go to" in command:
            site = command.replace("open website", "").replace("go to", "").strip()
            if site:
                if not site.startswith("http"):
                    site = site.replace(" ", "")
                    url = f"https://{site}.com"
                else:
                    url = site
                webbrowser.open(url)
                speak(f"Opening {url}")
            else:
                speak("Please specify the website you want to open.")
        
        else:
            # If no command matches, search on Google
            google_search(command)
                    
if __name__ == "__main__":
    main()