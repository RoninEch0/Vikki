import socket
import subprocess
import re
import time




def connexion(instance_robot) :
    
    instance_robot.active_window = 'screen_loading_wifi_connection'
    is_connected = test_internet_connection()
    while is_connected == False :
        instance_robot.active_window = 'screen_loading_no_wifi'
        time.sleep(3)
        instance_robot.list_wifi = [] #get_list_wifi_available()
        if instance_robot.list_wifi :
            instance_robot.active_window = 'screen_wifi_connection_select'
            #LA BOUCLEEEEEEEEEE
            while (instance_robot.active_wifi == '' or instance_robot.active_wifi_password == ''):
                time.sleep(1)
            instance_robot.active_window = 'screen_loading_wifi_connection'
            is_connected = connect_wifi(instance_robot.active_wifi,instance_robot.active_wifi_password)

            
    
    
        


def test_internet_connection():
    try:
        # Essayez de se connecter à un serveur distant (par exemple, google.com) sur le port 80
        socket.create_connection(("www.google.com", 80), timeout=10)
        print("Connexion Internet réussie.")
        return True
    except OSError:
        print("Échec de la connexion Internet.")
        return False

def get_country_code():
    result = subprocess.run(['iw', 'reg', 'get'], capture_output=True, text=True)
    match = re.search(r'country ([A-Za-z]{2})', result.stdout)
    if match:
        return match.group(1)
    else:
        return None

def get_list_wifi_available() -> str:
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

def connect_wifi(ssid, mot_de_passe) -> bool:
    try:
        # Connexion au réseau Wi-Fi
        connect_result = subprocess.run(f"nmcli device wifi connect {ssid} password {mot_de_passe}", shell=True, capture_output=True, text=True)
        if connect_result.returncode == 0:
            return True
        else:
            instance_robot.active_window = 'screen_wifi_no_connection'
            instance_robot.active_wifi = ''
            instance_robot.active_wifi_password = ''
            time.sleep(3)
            return False

    except:
        return False










