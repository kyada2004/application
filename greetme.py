import pyttsx3
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",200)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greetMe(hour):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        greeting = "Good Morning, sir"
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon, sir"
    elif hour >= 18 and hour <= 21:
        greeting = "Good Evening, sir"
    else:
        greeting = "Good Night, sir"
    
    greeting += ". Please tell me, how can I help you?"
    return greeting

