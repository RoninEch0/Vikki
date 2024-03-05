import os
import threading
import time
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import supp_output
import sounddevice

class Microphone:
    def __init__(self):
        self.recognizer=sr.Recognizer()
        self.thread_microphone=threading.Thread(target=self.microphone_run)
        self.active_microphone = False
        self.speech_string=''
        self.is_speech=False
       
    def thread_microphone_start(self):
        self.active_microphone=True
        self.thread_microphone.start()
        
    def thread_microphone_stop(self):
        self.active_microphone=False
        self.thread_microphone.join()
    
    def get_speech_string(self)->str:
        value = self.speech_string
        self.is_speech=True
        return value
    
    def set_speech_string(self,value):
        self.speech_string=value
    
    
    def microphone_run(self):
        while self.active_microphone:
            self.is_speech=False
            with sr.Microphone() as source:
                try:
                    self.speech_string = self.recognizer.recognize_google(self.recognizer.listen(source), language='fr-FR')
                except:
                    pass
            print(self.speech_string)
            
            """while not self.is_speech:
                time.sleep(1)
            self.speech_string=''
            """
            
                