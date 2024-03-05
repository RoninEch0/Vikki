
import threading
import time

class Speaker:
    def __init__(self):
        self.active_speaker=False
        self.thread_speaker=threading.Thread(target=self.speaker_run)
        self.speech_string=""        
        
    
    def thread_speaker_start(self):
        self.active_speaker=True
        self.thread_speaker.start()
        
    def thread_speaker_stop(self):
        self.active_speaker=False
        self.thread_speaker.join()
        
    def set_speech_string(self,value):
        self.speech_string=value
        
    def speaker_run(self):
        while self.active_speaker:
            if self.speech_string!="":
                tts = gTTS(text=response_text, lang="fr", slow=False)
                tts.save("/home/raspberry/Desktop/Projet_Vikki/assets/vc_output.mp3")
                with supp_output.suppress_stdout_stderr():
                    play(AudioSegment.from_mp3("/home/raspberry/Desktop/Projet_Vikki/assets/vc_output.mp3"))
                self.speech_string=""
                    
    
