import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
from wikipedia import exceptions
import webbrowser
import os
import pandas as pd
# import __test
from openai import OpenAI
chatStr = ""
def chat(query):
    global chatStr
    chatStr += f"Mickey: {query}\n Asistant: "
    print(chatStr)
    client = OpenAI(api_key='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')



    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": f"{chatStr}"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        # print(response.choices[0].message.content)
        speak(response.choices[0].message.content)
        chatStr += f"{response.choices[0].message.content}\n"
        return chatStr
    except Exception as e:
            print(e)
            return None
def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[1].id)
    print(f"Speaking: {audio}")
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't recognize that. Say that again please...")
            return "None"

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir..")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir..")
    else:
        speak("Good Evening Sir..")
    speak("I am your asistant. sir, Please tell me how may help you?..")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        if query !='None':
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
            if "open" in query:
                for site in sites:
                    if f"open {site[0]}".lower() in query.lower():
                        speak(f"Opening {site[0]} sir...")
                        webbrowser.open(site[1])
            elif "play music" in query:
                musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
                os.system(f"open {musicPath}")
            elif "reset chat".lower() in query.lower():
                chatStr = ""

            elif 'exit' in query:
                speak('okey sir.. exit')
                break
            else:
                print("Chatting...")
                chat(query)
