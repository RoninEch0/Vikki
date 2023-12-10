#Import du fichier

import sys
sys.path.insert(1, '/home/raspberry/Desktop/Projet Vikki/Screen')

#import librairie
import time
import pygame
import threading

#import fichier python
import initialisation
import dispose
import robot
import screen
import camera_facedetection
import internet
import vocal_command



def main() -> None :
    
    Vikki = robot.Robot()
    
    #INITIALISATION :
    initialisation.initialisation_all(Vikki)
    
    Vikki.active_window = 'screen_loading_init'
    thread_screen = threading.Thread(target=screen.screen_manager,args = (Vikki,))
    thread_screen.start()
    time.sleep(1)
    
    thread_vc = threading.Thread(target=vocal_command.vc_robot,args = (Vikki,))
    thread_vc.start()
    """

    internet.connexion(Vikki)

    Vikki.active_window = 'screen_loading_init'

    thread_screen = threading.Thread(target=screen.screen_manager,args = (Vikki,))
    thread_screen.start()
    
    time.sleep(5)
    
    Vikki.active_camera = True
    
    thread_camera = threading.Thread(target=camera_facedetection.camera_face_detection,args = (Vikki,)) # Demarrer la camera AVANT SCREEN_EYE_WATCHING
    thread_camera.start()
    
    Vikki.active_window = 'screen_eye_watching'
    #---Fonctionnement
    time.sleep(10)
    Vikki.active_camera = False
    thread_camera.join()
    """
    time.sleep(60)
    Vikki.active_window = ''
    thread_screen.join()
    Vikki.active_vc=False
    thread_vc.join()
    
    
    #FIN D'EXECUTION
    dispose.Dispose_all()
    
    


if __name__ == "__main__":
    main()