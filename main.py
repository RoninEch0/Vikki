
import sys 
sys.path.append('/home/raspberry/Desktop/Projet_Vikki/src/')
sys.path.append('/home/raspberry/Desktop/Projet_Vikki/utils/')
import yaml


import screen
import camera
import microphone
import robot
import speaker
import medical_sensor

def extract_config()-> map:
    config_yaml="/home/raspberry/Desktop/Projet_Vikki/config/config.yaml"
    with open(config_yaml, 'r') as fichier_yaml:
        config = yaml.safe_load(fichier_yaml)
    return(config)

def main() -> None :
    config_map=extract_config()
    screen_vikki=screen.Screen(config_map["screen"])
    camera_vikki=camera.Camera()
    microphone_vikki=microphone.Microphone()
    speaker_vikki=speaker.Speaker()
    medical_sensor_vikki=medical_sensor.Medical_Sensor()
    vikki=robot.Robot(screen_vikki,camera_vikki,microphone_vikki,speaker_vikki,medical_sensor_vikki)
    vikki.run_robot()
    
if __name__ == "__main__":
    main()
