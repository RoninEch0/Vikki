
import sys 
sys.path.append('/home/raspberry/Desktop/Projet_Vikki/src/')
import yaml


import screen
import camera
import robot

def extract_config()-> map:
    config_yaml="/home/raspberry/Desktop/Projet_Vikki/config/config.yaml"
    with open(config_yaml, 'r') as fichier_yaml:
        config = yaml.safe_load(fichier_yaml)
    return(config)

def main() -> None :
    config_map=extract_config()
    screen_vikki=screen.Screen(config_map["screen"])
    camera_vikki=camera.Camera()
    vikki=robot.Robot(screen_vikki,camera_vikki)
    vikki.run_robot()
    
if __name__ == "__main__":
    main()
