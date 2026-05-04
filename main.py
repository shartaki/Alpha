import pyttsx3 as p 
from selenum_web import WikipediaSearch
from yt_audio import MusicPlayer
from text import object_detection_and_speech
from news import news
import webbrowser
#from readthetextweb import *
# import randfacts
import datetime
import os
from weather import *
import speech_recognition as sr

engine = p.init()
rate=engine.getProperty('rate')
engine.setProperty('rate',190)
voices=engine.getProperty('voices')
print(voices)
# engine.setProperty('voices', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>0 and hour < 12:
        return("morning")
    elif hour>=12 and hour< 16:
        return("afternoon")
    else:
        return("evening")

today_date=datetime.datetime.now()
r = sr.Recognizer()

speak(" hello sir good " + wishme() + " i'm your  personal  assistant  alpha ")
#speak(" today is "+ today_date.strftime("%d")+ " of " + today_date.strftime("%B") + " And its currently " + (today_date.strftime("%I"))+ (today_date.strftime("%M"))+(today_date.strftime("%p")))
#speak(" Temparature in your location is "+ str(temp()) + " degree celsius " + " and with " + str(des()) )
#speak(" how are you ")
speak(" what  can i do for you ? ")

with sr.Microphone() as source:
    r.energy_threshold=10000 
    r.adjust_for_ambient_noise(source,1.2)
    print("listening")
    audio = r.listen(source)
    text= r.recognize_google(audio)
    print(text)
if "what" and "about" "you" in text:
    speak(" i am also having a good day sir ")

speak(" what can i do for you ? ")

with sr.Microphone() as source:
    r.energy_threshold=10000
    r.adjust_for_ambient_noise(source,1.2)
    print("listening")
    audio = r.listen(source)
    text2 = r.recognize_google(audio)

if "information" in text2:
    speak("you need information related in which topic ")

    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening")
        audio = r.listen(source)
        information= r.recognize_google(audio)
    speak("searching {} in wikipedia".format(information))

    assist = WikipediaSearch()
    assist.get_info(information)

elif "play" and "video" in text2:
    speak("you want me to play which video ?")
    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening")
        audio = r.listen(source)
        vid= r.recognize_google(audio)
    speak("playing {} on youtube".format(vid))
    assist = MusicPlayer()
    assist.play(vid)
    
elif "scan" in text2:
    speak("you want know what in front of you ?")
    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening")
    speak("scanning what are things in front of you")
    object_detection_and_speech()


elif "news"  in text2:
    speak("Sure sir, now i will read news for you ")
    arr =news()
    for i in range(len(arr)):
        print(arr[i])
        speak(arr[i])
        
#elif "fact" or "facts" in text2:
#    speak("Sure sir , ")
#    x=randfacts.get_fact()
#    print(x)
#    speak("did you know that , "+x)
