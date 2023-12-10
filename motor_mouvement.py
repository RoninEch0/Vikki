#FICHIER Des Mouvements DU ROBOT


#Import du fichier
import RPi.GPIO as GPIO
import parametrage

def Mouvement_Forward(Vikki)->str:
    try :
        GPIO.output(Vikki.motor_right_1, GPIO.LOW)
        GPIO.output(Vikki.Parametrage_Pin_Rasp('motor_right_2'), GPIO.HIGH)
        GPIO.output(Vikki.Parametrage_Pin_Rasp('motor_left_3'), GPIO.LOW)
        GPIO.output(Vikki.Parametrage_Pin_Rasp('motor_left_4'), GPIO.HIGH)
        return 'Mouvement Robot : Avance'

    except:
        return 'Mouvement Robot : ERROR in Forward'

def Mouvement_Backward()->str:
    try :
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_1'), GPIO.HIGH)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_2'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_3'), GPIO.HIGH)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_4'), GPIO.LOW)
        return 'Mouvement Robot : Recule'

    except:
        return 'Mouvement Robot : ERROR in Backward'

def Mouvement_Turn_Left()->str:
    try :
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_1'), GPIO.HIGH)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_2'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_3'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_4'), GPIO.LOW)
        return 'Mouvement Robot : TOURNE - GAUCHE'

    except:
        return 'Mouvement Robot : ERROR in Turn_Left'

def Mouvement_Turn_Right()->str:
    try :
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_1'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_2'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_3'), GPIO.HIGH)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_4'), GPIO.LOW)
        return 'Mouvement Robot : TOURNE - DROITE'

    except:
        return 'Mouvement Robot : ERROR in Turn_RIGHT'


def Mouvement_Stop()->str:
    try :
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_1'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_right_2'), GPIO.LOW)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_3'), GPIO.HIGH)
        GPIO.output(parametrage.Parametrage_Pin_Rasp('motor_left_4'), GPIO.LOW)
        return 'Mouvement Robot : TOURNE - DROITE'

    except:
        return 'Mouvement Robot : ERROR in Turn_RIGHT'
    
