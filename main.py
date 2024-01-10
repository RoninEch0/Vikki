
import sys 
sys.path.append('/home/raspberry/Desktop/Projet Vikki/code/')
import yaml


import screen
import robot


def main() -> None :
    config_yaml="/home/raspberry/Desktop/Projet Vikki/config/config.yaml"
    screen_vikki=screen.Screen(config_yaml)
    vikki=robot.Robot(screen_vikki)
    vikki.run_robot()
    
if __name__ == "__main__":
    main()
