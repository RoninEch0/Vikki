import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def vc_robot(instance_robot):
    recognizer = sr.Recognizer()
    instance_robot.active_vc = True
    while instance_robot.active_vc :
        is_talking_to_vikki = False
        text = ''
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            speech_string = recognizer.recognize_google(audio, language='fr-FR')
            if 'ok Vicky' in speech_string:
                is_talking_to_vikki = True
        except :
            pass
                
            # Ajoutez ici le traitement que vous souhaitez faire avec le texte transcrit
        """    
        except sr.UnknownValueError: #AVOIR CE QU IL FAUT FAIRE DE CETTE PARTIR (activation inutile si on a pas parler au robot?)
            text ="Désolé, je n'ai pas compris ce que vous avez dis."
        except sr.RequestError :
            text ="Désolé, une erreur est survenue. Si cela persiste veuillez contacter une aide"
        """ 
        if is_talking_to_vikki :
            
            
            
            
            tts = gTTS(text=text, lang="fr", slow=False)
            tts.save("vc_output.mp3")
            son = AudioSegment.from_mp3("vc_output.mp3")
            play(son)
                
            
