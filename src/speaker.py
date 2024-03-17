import sounddevice
import threading
import time
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS

class Speaker:
    def __init__(self):
        self.active_speaker=False
        self.thread_speaker=threading.Thread(target=self.speaker_run)
        self.speaker_queue=[]
        
    
    def thread_speaker_start(self):
        self.active_speaker=True
        self.thread_speaker.start()
        
    def thread_speaker_stop(self):
        self.active_speaker=False
        self.thread_speaker.join()
        
    def add_to_speaker_queue(self,value):
        self.speaker_queue.append(value)
        
    def speaker_run(self):
        while self.active_speaker:
            if self.speaker_queue!=[]:
                tts = gTTS(text=self.speaker_queue[0], lang="fr", slow=False)
                tts.save("/home/raspberry/Desktop/Projet_Vikki/assets/vc_output.mp3")
                play(AudioSegment.from_mp3("/home/raspberry/Desktop/Projet_Vikki/assets/vc_output.mp3"))
                self.speaker_queue.pop(0)
                
                    
    
