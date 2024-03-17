import time
import socket
import subprocess
import re
import openai

import logging


class Robot:
    def __init__(self,screen,camera,microphone,speaker,medical_sensor,lidar):
        self.screen=screen
        self.camera=camera
        self.microphone=microphone
        self.speaker=speaker
        self.medical_sensor=medical_sensor
        self.lidar=lidar
        
        self.messages=[{"role": "system", "content": "tu es un robot appel Vikki, tu es une assistante medicale. Donnes des reponses courtes et empathique. Tu peux etre philosophique"},]
        self.time_rest=0
        self.timer_for_rest=60*15
        
        
        self.is_robot_run=True
        self.analyse_run=False
            
    def run_robot(self):
        
        self.screen.thread_screen_start()
        time.sleep(3)
        self.connect_wifi()
        
        self.camera.thread_camera_start()
        self.screen.set_active_window('screen_eye_watching')

        self.speaker.thread_speaker_start()
        self.microphone.thread_microphone_start()
        self.medical_sensor.thread_medical_sensor_start()
        self.lidar.thread_lidar_start()
        
        while self.is_robot_run:
            
            self.screen.set_iris_eye_pos(self.camera.get_face_detected())

            if self.analyse_run:
                self.launch_analyse()
                self.analyse_run=False
            
            microphone_data_queue=self.microphone.get_speech_queue()
            if microphone_data_queue != []:
                for msg in microphone_data_queue:
                    response_vc=self.vocal_command(msg)
                    self.speaker.add_to_speaker_queue(response_vc)
                    microphone_data_queue=[]
                
            
            """
            self.screen.set_iris_eye_pos(self.camera.get_face_detected())
            data_vital=self.medical_sensor.get_bpm_spo2()
            data_lidar=self.lidar.get_data_lidar_list()
            
            if self.is_analyse:
                print("debut analyse")
                analyse_func(self)
                
            if !self.is_analyse:
                microphone_data_queue=self.microphone.get_speech_queue()
                if microphone_data_queue != []:
                    for msg in microphone_data_queue:
                        response_vc=self.vocal_command(msg)
                        self.speaker.add_to_speaker_queue(response_vc)
                        microphone_data_queue=[]
            """        
        self.speaker.thread_speaker_stop()
        self.lidar.thread_lidar_stop()
        self.microphone.thread_microphone_stop()
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
        print("vc input : "+vc_speech_string)
        if time.time()>self.time_rest:
            self.messages=[{"role": "system", "content": "tu es un robot qui porte le nom : Vikki. Tu es une assistante medicale. Donnes des reponses courtes et empathique. Tu peux etre philosophique"},]
        self.time_rest=time.time()+self.timer_for_rest
        response_text = ""
        match vc_speech_string:
            case " éteins-toi":
                self.is_robot_run=False
                response_text="C'est d'accord, je m'éteins. Au revoir."
            case "ok Vicky déplace-toi":
                response_text="Bien, je me déplace."
            case "ok Vicky arrête-toi":
                response_text="D'accord. J'arrête de me déplacer"
            case " lance une analyse":
                self.analyse_run=True
                response_text="Bien, je lance une analyse!"
            case _:
                self.messages.append({"role":"user","content":vc_speech_string})
                response_text=self.send_to_chatgpt_request()
        print("vc output : "+response_text)
        return(response_text)
    
    def send_to_chatgpt_request(self):
        completion = self.client.chat.completions.create(model="gpt-3.5-turbo",messages=self.messages)
        response=completion.choices[0].message.content
        self.messages.append({"role":"assistant","content":response})
        return response
    
    def launch_analyse(self):
        self.speaker.add_to_speaker_queue("Sur une échelle de 1 à 10, 10 étant un très bonne état de santé, comment vous-sentez vous?")
        time.sleep(1)
        self.screen.set_active_window('analyse_score_question')
        score_analyse=0
        while score_analyse==0:
            score_analyse=self.screen.get_score_analyse()
            if score_analyse == 0:
                microphone_answer = self.microphone.get_speech_queue()
                if microphone_answer != []:
                    score_analyse= microphone_answer[0][1:]
        self.speaker.add_to_speaker_queue("Vous avez répondu "+str(score_analyse))
        time.sleep(1)
        self.speaker.add_to_speaker_queue("Je souhaite prendre vos constantes vitales basiques pour votre examen, placer votre main sur ma tete s'il vous plait")
        self.screen.set_active_window('analyse_vital')
        self.medical_sensor.reset_bpm_spo2()
        data_medical_sensor=self.medical_sensor.get_bpm_spo2()
        while data_medical_sensor['bpm']==[] or data_medical_sensor['spo2']==[]:
            data_medical_sensor=self.medical_sensor.get_bpm_spo2()
        self.screen.set_active_window('analyse_vital_value')
        while len(data_medical_sensor['bpm'])<15 and len(data_medical_sensor['spo2'])<15:
            self.screen.set_bpm_spo2(data_medical_sensor['bpm'][-1],data_medical_sensor['spo2'][-1])
            data_medical_sensor=self.medical_sensor.get_bpm_spo2()
        self.speaker.add_to_speaker_queue("l'analyse estr fini. Merci!")
        self.screen.set_active_window('screen_eye_watching')


                
        
        
        
        
        
        
        
    