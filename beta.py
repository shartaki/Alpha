import pyttsx3 as p
from selenum_web import WikipediaSearch
from text import object_detection_and_speech
from news import news
from weather import *
import webbrowser
import datetime 
from face import *
from datacollect import *
from weather import *
import os 
import speech_recognition as sr
from read_txt import capture_and_read_text  # Importing the function
from yt_audio import MusicPlayer

def initialize_engine():
    engine = p.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 200)
    voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)  # Correct property name
    return engine

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "morning"
    elif 12 <= hour < 16:
        return "afternoon"
    else:
        return "evening"

def get_date_time():
    return datetime.datetime.now()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

def main():
    engine = initialize_engine()
    speak(engine, "Hello sir, good " + wish_me() + ", I'm your personal assistant, Alpha.")
    speak(engine, "Say 'Hey Alpha' to start.")
    while True:
        print("Say 'Hey Alpha' to start.")
        text = listen()
        if text and "hey alpha" in text:
            speak(engine, "Yes, how can I help you?")
            print( "Yes, how can I help you?")
            while True:
                text2 = listen()
                
                if text2:
                    if "stop listening" in text2:
                        speak(engine, "Goodbye!")
                        print("Goodbye!")
                        return
                    if "information" in text2:
                        speak(engine, "You need information related to which topic?")
                        information = listen()
                        if information:
                            speak(engine, f"Searching {information} on Wikipedia.")
                            assist = WikipediaSearch()  # Ensure this class is correctly implemented
                            assist.get_info(information)
                    elif "how are you " in text2:
                        speak(engine," I'm fine sir ")
                        print(" I'm fine sir ")
                    
                    elif "what is your name" in text2:
                        speak(engine," my name is Alpha ")
                        print(" my name is Alpha ")
                    elif "play video" in text2:
                        speak(engine, "You want me to play which video?")
                        vid = listen()
                        if vid:
                            speak(engine, f"Playing {vid} on YouTube.")
                            assist = MusicPlayer()  # Ensure this class is correctly implemented
                            assist.play(vid)
                        
                    elif "weather" in text2:
                        speak(engine," Temparature in your location is "+ str(temp()) + " degree celsius " + " and with " + str(des()) )
                        print(" Temparature in your location is "+ str(temp()) + " degree celsius " + " and with " + str(des()))
                    elif "scan" in text2:
                        speak(engine, "You want to know what is in front of you?")
                        speak(engine, "Scanning what are the things in front of you.")
                        object_detection_and_speech()
                    elif "time" in text2:
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                        speak(engine,"Sir, the time is {strTime}".format(strTime=strTime))
                        print("Sir, the time is {strTime}".format(strTime=strTime))
                    elif "news" in text2:
                        speak(engine, "Sure sir, now I will read the news for you.")
                        arr = news()
                        for item in arr:
                            print(item)
                            speak(engine, item)
                            print(item)
                    elif "read text" in text2:
                        speak(engine, "opening the camera , capture the image")
                        capture_and_read_text()
                    elif "add face" in text2:
                        speak(engine, "Adding new face into your database.")
                        collect_and_train_faces()
                    
                    elif "recognise the face" in text2:
                        speak(engine, "Recognizing the face.")
                        face_recognition()
                    else:
                        speak(engine, "Sorry, I did not catch that. Please repeat.")
                else:
                    speak(engine, "Sorry, I did not catch that. Please repeat.")

if __name__ == "__main__":
    main()   
