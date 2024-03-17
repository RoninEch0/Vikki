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
        self.speech_queue=[]
       
    def thread_microphone_start(self):
        self.active_microphone=True
        self.thread_microphone.start()
        
    def thread_microphone_stop(self):
        self.active_microphone=False
        self.thread_microphone.join()
    
    def get_speech_queue(self):
        value = self.speech_queue
        self.speech_queue=[]
        return value
    
    def reset_speech_queue(self):
        self.speech_queue=[]

    def microphone_run(self):
        while self.active_microphone:
            speech_string=""
            with sr.Microphone() as source:
                try:
                    speech_string = self.recognizer.recognize_google(self.recognizer.listen(source), language='fr-FR')
                except:
                    pass
                if 'ok Vicky' in speech_string[:8]:
                    self.speech_queue.append(speech_string[8:])
                    
            
                