import speech_recognition as sr  # type: ignore
import webbrowser  # type: ignore
import pyttsx3  # type: ignore
import musicLibrary  # type: ignore
import requests  # type: ignore
from gtts import gTTS  # type: ignore
import pygame  # type: ignore
import os  # type: ignore
import json  # type: ignore

recognizer = sr.Recognizer() # type: ignore
engine = pyttsx3.init()  # type: ignore
newsapi = "<Your newsapi key>"

def speak_old(text):  # type: ignore
    engine.say(text)  # type: ignore
    engine.runAndWait()  # type: ignore

def speak(text):  # type: ignore
    tts = gTTS(text)  # type: ignore
    tts.save('temp.mp3')  # type: ignore
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):  # type: ignore # UPDATED FUNCTION
    headers = {
        "Authorization": "Api-key here",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",  # Optional
        "X-Title": "Zara Assistant"  # Optional
    }

    data = { # type: ignore
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "I'm sorry, I couldn't process that."

def processCommand(c):  # type: ignore
    if "open google" in c.lower(): # type: ignore
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower(): # type: ignore
        webbrowser.open("https://facebook.com")
    elif "open YouTube" in c.lower(): # type: ignore
        webbrowser.open("https://YouTube.com")
    elif "open linkdin" in c.lower(): # type: ignore
        webbrowser.open("https://linkdin.com")
    elif c.lower().startswith("play"): # type: ignore
        song = c.lower().split(" ")[1] # type: ignore
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower(): # type: ignore
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(c) # type: ignore
        speak(output)

if __name__ == "__main__":
    speak("Initializing Zara...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listing zara....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1) # type: ignore
            word = r.recognize_google(audio) # type: ignore
            if (word.lower() == "zara"): # type: ignore
                speak("Yes")
                with sr.Microphone() as source:
                    print("zara active ...")
                    audio = r.listen(source) # type: ignore
                    commmand = r.recognize_google(audio) # type: ignore
                    processCommand(commmand) # type: ignore
        except Exception as e:
            print("Error; {0}".format(e))
