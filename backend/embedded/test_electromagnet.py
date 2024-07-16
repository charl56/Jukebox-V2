#!/usr/bin/python3
### FICHIER DE TEST 
# Installer keyboard avec la commande:  install keyboard
# Executer le programme depuis la raspberry, avec clavier branché dessus

import RPi.GPIO as GPIO
import keyboard                # Importer la bibliotheque de gestion du clavier

# Utilisez le numéro de pin correct selon votre schéma électrique
ELECTRO_MAGNET = 26
ENTER_KEY = False

GPIO.setmode(GPIO.BCM)         # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)        # Ne pas tenir comte des alertes
GPIO.setup(ELECTRO_MAGNET, GPIO.OUT)  # Définir le pin comme sortie


def electro_magnet_on():
    """
    Function to active electromagnet 
    """
    GPIO.output(ELECTRO_MAGNET, GPIO.HIGH)  # Activer l'électroaimant

def electro_magnet_off():
    """
    Function to desactive electromagnet 
    """
    GPIO.output(ELECTRO_MAGNET, GPIO.LOW)  # Désactiver l'électroaimant
    



# Garder le programme en exécution pour écouter les événements de clavier
print("Appuyez sur les flèches haut et bas pour déplacer le moteur. Appuyez sur 'q' pour quitter.")
while True:
    if keyboard.is_pressed("q"):
        print("Quitter le programme.")
        GPIO.cleanup()
        break
	
    if keyboard.is_pressed("enter"):
        ENTER_KEY = not ENTER_KEY
        if ENTER_KEY:
            electro_magnet_on()
        else:
            electro_magnet_off()
