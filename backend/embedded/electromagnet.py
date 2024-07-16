from config import ELECTRO_MAGNET
import RPi.GPIO as GPIO

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
    