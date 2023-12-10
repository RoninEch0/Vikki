#FICHIER INITIALISATION DU ROBOT

#import librairie
import RPi.GPIO as GPIO
import pygame

#import fichier python
import robot

#Fonction d'initialisation du ROBOT
def initialisation_all(instance_robot):
    
    print("Début de l'initialisation")
    
    print("Initialisation des pins ")
    print(initialisationp_pin_rasp(instance_robot))
    
    
    #---autres init
    
    print("Fin de l'initialisation")
    pass


#Fonction d'initialisation des pin de la Raspberry pi 4
def initialisationp_pin_rasp(instance_robot) -> str:
    
    try :
        #activation des pins en mode BOARD (c'est à dire que la pin est désigner par son numéro d'emplacement pin_numéro 11 = GPIO 17)
        GPIO.setmode(GPIO.BOARD)
        #Setup des pin (attribution des pins)
        GPIO.setup(instance_robot.motor_right_1, GPIO.OUT)
        GPIO.setup(instance_robot.motor_right_2, GPIO.OUT)
        GPIO.setup(instance_robot.motor_left_3, GPIO.OUT)
        GPIO.setup(instance_robot.motor_left_4, GPIO.OUT)
        return 'GPIO SETUP : OK'
    
    except :
        return 'GPIO SETUP : ERROR in init'
    
#Fonction d'initialisation de l'écran de la Raspberry pi 4
def initialisation_pygame_screen(instance_robot) -> str :
    
    try :
        # Initialisation de Pygame
        pygame.init()
        fenetre = None
        if instance_robot.fullscreen:
            fenetre = pygame.display.set_mode((instance_robot.largeur, instance_robot.hauteur), pygame.FULLSCREEN)  # Utilisation du drapeau FULLSCREEN
        else:
            fenetre = pygame.display.set_mode((instance_robot.largeur, instance_robot.hauteur))
        instance_robot.window = fenetre

        pygame.display.set_caption(instance_robot.title_caption)
        
        return 'SCREEN SETUP : OK'
    
    except :
        return 'SCREEN SETUP : ERROR in init'
    

        
    



