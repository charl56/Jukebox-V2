#!/usr/bin/python3
### FICHIER DE TEST 
# Installer keyboard avec la commande:  install keyboard
# Executer le programme depuis la raspberry, avec clavier branché dessus
import RPi.GPIO as GPIO
import keyboard                # Importer la bibliotheque de gestion du clavier
import time

# Configuration des pins GPIO
servo_pin = 18  # Pin GPIO auquel le servomoteur est connecté

# Configuration du mode de numérotation des pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Initialisation du signal PWM à 50Hz
pwm = GPIO.PWM(servo_pin, 50)  # Fréquence de 50Hz
pwm.start(0)  # Démarrer le PWM avec un cycle de service de 0

def moveZToAngle(angle):
    duty = 2 + (angle / 18)  # Calcul du cycle de service correspondant à l'angle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.2)  # Temps pour laisser le servomoteur atteindre la position
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)



# Garder le programme en exécution pour écouter les événements de clavier
print("Appuyez sur les flèches haut et bas pour déplacer le moteur. Appuyez sur 'q' pour quitter.")
while True:
    if keyboard.is_pressed("q"):
        print("Quitter le programme.")
        GPIO.cleanup()
        break
	
    if keyboard.is_pressed("a"):
        moveZToAngle(0)
    if keyboard.is_pressed("z"):
        moveZToAngle(90)
    if keyboard.is_pressed("e"):
        moveZToAngle(180)	
