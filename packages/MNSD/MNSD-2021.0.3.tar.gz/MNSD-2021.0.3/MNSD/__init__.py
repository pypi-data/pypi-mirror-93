from pytube import YouTube
from PrtSc.PrtSc import PrtSc
from OS_Platform.OS_Platform import getOSPlatform
import psutil
import matplotlib.pyplot as plt
import matplotlib
from batterycharge.batterycharge import getBatteryCharge
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from cv2 import imshow,VideoCapture,waitKey,destroyAllWindows
from pyjokes import get_joke
import flask
import rotatescreen
import pyautogui
import sqlite3
import pyttsx3
import requests
import json
from HCF import HCF
class Joke:
    def __init__(self):
        self.joke=get_joke()

    def print(self):
        print(self.joke)

    def say(self,accent):
        x=TextToSpeechInit()
        x.setAccent(accent)
        x.speak(self.joke)

class openWebcam:
    def __init__(self,codeorkey):
        cam=VideoCapture(0)
        while True:
            check,frame=cam.read()
            imshow("Frame",frame)
            key=waitKey(1)
            if key==codeorkey:
                break

        cam.release()
        destroyAllWindows()


class YoutubeVideo:
    def __init__(self,url):
        self.url=url

    def download(self):
        o=YouTube(self.url)
        vid=o.streams.get_by_itag(22)
        vid.download()

    def openVideo(self):
        webbrowser.open(self.url)


class getLocation:
    def __init__(self):
        self.details=requests.get('https://ipinfo.io/')
        self.locationdata=self.details.json()

class DateError(BaseException):
    def __init__(self):
        print("Invalid Date Given.")

def dayOnDate(d,m,y):
    disallowed=[
        d>31,
        m>12
    ]
    if any(disallowed):
        raise DateError

    monthcodes=[0,3,3,6,1,4,6,2,5,0,3,5]
    rem=(y//100)%4
    ccode=0
    if rem==1:
        ccode=5
    elif rem==2:
        ccode=3
    elif rem==3:
        ccode=1

    leap=0
    if y%4==0 and y%100!=0 and m>2:
        leap=1
    elif y%400==0 and m>2:
        leap=1
    else:
        pass
    daycode=(d+monthcodes[m-1]+(y%100)-1+((y%100)-1)//4+ccode+leap)%7
    days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    return days[daycode]

class AccentError(BaseException):
    def __init__(self):
        print("invalid Accent Name... Exiting...")

class TextToSpeechInit:
    def __init__(self):
        self.speaker=pyttsx3.init()
        self.accent='male'
        self.voices=self.speaker.getProperty('voices')
        self.speaker.setProperty('voice', self.voices[0].id)

    def setAccent(self,accent):
        self.accent=accent.lower()
        if self.accent!='male' and self.accent!='female':
            raise AccentError
        if self.accent=='female':
            self.speaker.setProperty('voice',self.voices[1].id)
        else:
            self.speaker.setProperty('voice', self.voices[0].id)

    def speak(self,msg):
        self.speaker.say(msg)
        self.speaker.runAndWait()




