#Import du fichier
import RPi.GPIO as GPIO
import time

# Configuration des numéros de broche en mode BOARD
GPIO.setmode(GPIO.BOARD)

# Numéro de la broche que vous souhaitez activer en mode BOARD (11 correspond à GPIO 17 en mode BCM)

pin_num1 = 16
pin_num2 = 18
pin_num3 = 13
pin_num4 = 15

# Configuration de la broche en mode de sortie
GPIO.setup(pin_num1, GPIO.OUT)
GPIO.setup(pin_num2, GPIO.OUT)
GPIO.setup(pin_num3, GPIO.OUT)
GPIO.setup(pin_num4, GPIO.OUT)
"""
print('AVANCE')
GPIO.output(pin_num1, GPIO.LOW)
GPIO.output(pin_num2, GPIO.HIGH)
GPIO.output(pin_num3, GPIO.LOW)
GPIO.output(pin_num4, GPIO.HIGH)
time.sleep(5)

print('STOP')
GPIO.output(pin_num1, GPIO.LOW)
GPIO.output(pin_num2, GPIO.LOW)
GPIO.output(pin_num3, GPIO.LOW)
GPIO.output(pin_num4, GPIO.LOW)
time.sleep(5)
"""

print('RECULE')
GPIO.output(pin_num1, GPIO.HIGH)
GPIO.output(pin_num2, GPIO.LOW)
GPIO.output(pin_num3, GPIO.HIGH)
GPIO.output(pin_num4, GPIO.LOW)
time.sleep(10)

"""
print('AVANCE')
GPIO.output(pin_num1, GPIO.LOW)
GPIO.output(pin_num2, GPIO.HIGH)
GPIO.output(pin_num3, GPIO.LOW)
GPIO.output(pin_num4, GPIO.HIGH)
time.sleep(5)
"""
# Nettoyage des ressources GPIO
GPIO.cleanup()
