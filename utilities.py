import os
import random
import requests
from time import gmtime, strftime
import speech_recognition as sr
import pyaudio
import playsound
from gtts import gTTS
from flask_sqlalchemy import SQLAlchemy
from application import db
import models

current_user = None
readable= True
def getPray(args):
    '''
    url prams https://aladhan.com/prayer-times-api
    url example:  http://api.aladhan.com/v1/calendarByCity?city=London&country=UnitedKingdom&method=2&month=04&year=2017
    '''

    country = args[0]
    city = args[1]
    year = strftime("%Y", gmtime())
    month = strftime("%m", gmtime())

    url = "http://api.aladhan.com/v1/calendarByCity?city={}&country={}&method=5&month={}&year={}".format(city,country,month,year)
    r = requests.get(url=url).json()
    temp = r['data'][0]['timings']
    return temp

def getTafseerInRange(args):
    global readable
    readable = False
    tafseer_ID=int(args[0])
    sura_number=int(args[1])
    start_ayah_number=int(args[2])
    result=""
    for i in range(int(args[3])-int(args[2])+1):
        url = "http://api.quran-tafseer.com/tafseer/"+str(tafseer_ID)+"/"+ str(sura_number) +"/"+ str(start_ayah_number+i)
        tafseer = requests.get(url=url).json()
        result+="ayah number ("+str(start_ayah_number+i)+"):  "+tafseer['text']+" <br> "
    return result

def getText(args):
    global readable
    readable = False
    sura_number = int(args[0])
    start_ayah_number = int(args[1])
    result = ""
    for i in range(int(args[2]) - int(args[1]) + 1):
        url = "http://api.alquran.cloud/v1/ayah/" + str(sura_number) + ":" + str(start_ayah_number + i)
        tafseer = requests.get(url=url).json()
        result += "("+str(start_ayah_number + i)+")"+tafseer['data']['text']+" <br> "
    return result

def read(args):
    sura_number = int(args[0])
    start_ayah_number = int(args[1])
    result = ""
    for i in range(int(args[2]) - int(args[1]) + 1):
        url = "http://api.alquran.cloud/v1/ayah/" + str(sura_number) + ":" + str(start_ayah_number + i)+"/ar.alafasy"
        tafseer = requests.get(url=url).json()
        result += "(" + str(start_ayah_number + i) + ")" + tafseer['data']['text'] + " <br> "
    return result

def getMofasreen():
    global readable
    readable = False
    url = "http://api.quran-tafseer.com/tafseer"
    list=requests.get(url=url).json()
    counter=1
    result=""
    for i in list:
        result+=str(counter)+":  "+i['name']+" <br> "
        counter+=1
    return result

def audio():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        audio= r.listen(source,timeout=2,phrase_time_limit=5)
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')
        return voice_data

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"Imam: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file

db.create_all()
def register(args):
    try:
        reg = models.User(username=args[0], password=args[1])
        db.session.add(reg)
        global current_user
        current_user = models.chat(username=reg.username, body="")
        db.session.add(current_user)
        db.session.commit()
        return "Success"
    except SQLAlchemy.IntegrityError:
        return "Failed"

def add_chat(text):
    db.create_all()
    db.session.add(current_user)
    current_user.body += text
    db.session.commit()
    db.session.expire_on_commit = False

def login(args):
    user = models.User.query.filter_by(username=args[0]).first()
    if user != None:
        if args[1] == user.password:
            global current_user
            current_user=models.chat(username=args[0], body="")
            return "Success"
        else:
            return "Failed"
    else:
        return "Failed"

def read(args):
    sura_number = int(args[0])
    start_ayah_number = int(args[1])
    if(start_ayah_number != 1 or sura_number != 1):
        playsound.playsound("https://cdn.islamic.network/quran/audio/128/ar.alafasy/1.mp3")
    for i in range(int(args[2]) - int(args[1]) + 1):
        url = "http://api.alquran.cloud/v1/ayah/" + str(sura_number) + ":" + str(start_ayah_number + i)+"/ar.alafasy"
        tafseer = requests.get(url=url).json()
        audio=tafseer['data']['audioSecondary'][0]
        playsound.playsound(audio)
