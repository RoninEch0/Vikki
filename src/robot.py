import time
import socket
import subprocess
import re


class Robot:
    def __init__(self,screen,camera):
        self.screen=screen
        self.camera=camera
        
    def run_robot(self):
        self.screen.thread_screen_start()
        time.sleep(3)
        self.connect_wifi()
        self.screen.set_active_window('screen_eye_watching')
        self.camera.thread_camera_start()
        
        timer=time.time()+20
        while timer>time.time():
            self.screen.set_iris_eye_pos(self.camera.get_face_detected())
        
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
            else:
                return False

        except:
            return False
        
