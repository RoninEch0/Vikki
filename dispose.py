#FICHIER DISPOSE DU ROBOT


#import librairie
import RPi.GPIO as GPIO
import pygame
import sys


def Dispose_all():
    print("Début extinction programme")
    
    
    print("Nettoyage des pins de la Raspberry ")
    print(Clean_Pin_Rasp())
    
    #---autres dispose
    
    print("Extinction du programme")
    pass

def Clean_Pin_Rasp() -> str:
    try:
        GPIO.cleanup()
        return 'GPIO SETUP : CLEAR'
    except:
        return 'GPIO SETUP : ERROR in Clean'

def Clean_Screen() -> str:
    try:
        # Quitter Pygame et terminer le programme
        pygame.quit()
        return 'SCREEN SETUP : CLEAR'
    except:
        return 'SCREEN SETUP : ERROR in Clean'