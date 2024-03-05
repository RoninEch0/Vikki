import time
import socket
import subprocess
import re
import openai

import logging


class Robot:
    def __init__(self,screen,camera,microphone,speaker,medical_sensor):
        self.screen=screen
        self.camera=camera
        self.microphone=microphone
        self.speaker=speaker
        self.medical_sensor=medical_sensor
        
        self.client = openai.OpenAI(api_key="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")
        self.messages=[{"role": "system", "content": "tu es un robot appel Vikki, tu es une assistante medicale. Donnes des reponses courtes et empathique. Tu peux etre philosophique"},]
        self.time_rest=0
        self.timer_for_rest=60*15
        
    def run_robot(self):
        self.screen.thread_screen_start()
        time.sleep(3)
        self.connect_wifi()
        self.camera.thread_camera_start()
        self.screen.set_active_window('screen_eye_watching')
        
        
        '''
        self.speaker.thread_speaker_start()
        '''
        self.microphone.thread_microphone_start()
    
        
        self.medical_sensor.thread_medical_sensor_start()
        
        timer=time.time()+40
        while timer>time.time():
            self.screen.set_iris_eye_pos(self.camera.get_face_detected())
            #print(self.medical_sensor.get_bpm_spo2())
            time.sleep(1)
            
            microphone_text_spoke=self.microphone.get_speech_string()
            logging.info(microphone_text_spoke)
            '''
            if microphone_text_spoke != '':
                response_for_speaker=self.vocal_command(microphone_text_spoke)
                if response_for_speaker!="":
                    #######
            '''
        
        '''
        self.speaker.thread_speaker_stop()
        '''
        self.microphone.thread_vocal_command_stop()
        
        self.medical_sensor.thread_medical_sensor_stop()
        self.camera.thread_camera_stop()
        self.screen.thread_screen_stop()
    
    def connect_wifi(self):
        self.screen.set_active_window('screen_loading_wifi')
        is_connected =self.test_wifi_connect()
        while is_connected == False :
            self.screen.set_active_window('screen_loading_no_wifi')
            list_wifi= self.get_list_wifi_available()
            time.sleep(2)
            if list_wifi :
                self.screen.set_list_wifi(list_wifi)
                self.screen.set_active_window('screen_wifi_connection_select')
                self.screen.set_selected_wifi_name('')
                self.screen.set_selected_wifi_password('')
                selected_wifi_name,selected_wifi_password='',''
                while (selected_wifi_name == '' or selected_wifi_password == ''):
                    selected_wifi_name=self.screen.get_selected_wifi_name()
                    selected_wifi_password=self.screen.get_selected_wifi_password()
                self.screen.set_active_window('screen_loading_wifi')
                is_connected = self.connect(selected_wifi_name,selected_wifi_password)
        self.screen.set_active_window('screen_loading_wifi_valid')
        time.sleep(2)
        
    def test_wifi_connect(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=10)
            return True
        except OSError:
            return False
    
    def get_list_wifi_available(self) -> str:
        list_wifi=[]
        string_list_wifi=str(subprocess.run("sudo iwlist wlan0 scan | grep ESSID", shell=True, capture_output=True, text=True)).replace(' ','')
        while string_list_wifi.find('ESSID:')>-1 :
            string_list_wifi= string_list_wifi[string_list_wifi.find('ESSID:'):]
            index_beginning_name_wifi = string_list_wifi.find('"')+1
            index_end_name_wifi = string_list_wifi[index_beginning_name_wifi:].find('"')+index_beginning_name_wifi
            name_wifi = string_list_wifi[index_beginning_name_wifi:index_end_name_wifi]
            if name_wifi not in list_wifi :
                list_wifi.append(name_wifi)
            string_list_wifi=string_list_wifi[index_end_name_wifi:]
        return list_wifi
    
    def connect(self,ssid, password) -> bool:
        try:
            # Connexion au réseau Wi-Fi
            connect_result = subprocess.run(f"nmcli device wifi connect {ssid} password {password}", shell=True, capture_output=True, text=True)
            if connect_result.returncode == 0:
                return True
            return False

        except:
            return False
        
    def vocal_command(self,vc_speech_string):
        if time.time()>self.time_rest:
            self.messages=[{"role": "system", "content": "tu es un robot qui porte le nom : Vikki. Tu es une assistante medicale. Donnes des reponses courtes et empathique. Tu peux etre philosophique"},]
        if 'ok Vicky' in vc_speech_string:
            self.time_rest=time.time()+self.timer_for_rest 
            match vc_speech_string:
                case "ok Vicky éteins-toi":
                    response_text="C'est d'accord, je m'éteins. Au revoir."
                case "ok Vicky déplace-toi":
                    response_text="Bien, je me déplace."
                case "ok Vicky arrête-toi":
                    response_text="D'accord. J'arrête de me déplacer"
                case "ok Vicky lance une analyse":
                    response_text="Bien, je lance une analyse des constante vital"
                case _:
                    self.messages.append({"role":"user","content":speech_string_protected[8:]})
                    response_text=self.send_to_chatgpt_request()
                
            return(response_text)
        return("")
    
    def send_to_chatgpt_request(self):
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo",messages=self.messages)
        response=completion.choices[0].message.content
        self.messages.append({"role":"assistant","content":response})
        return response
                
        
