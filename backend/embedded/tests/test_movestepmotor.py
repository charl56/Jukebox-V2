#!/usr/bin/python3
### FICHIER DE TEST 
# Installer keyboard avec la commande:  install keyboard
# Executer le programme depuis la raspberry, avec clavier branché dessus

from time import sleep         # Importer la bibliotheque de gestion du temps 
import RPi.GPIO as GPIO        # Importer la bibliotheque de gestion des GPIO
import keyboard                # Importer la bibliotheque de gestion du clavier

# Commandes de pas, reliées aux GPIOs 14, 17, 24
L_STEP = 14     # Moteur branché en X, mais déplace en Y
R_STEP = 17     # Moteur branché en Y, déplace en Y
# Commandes de direction, reliées aux GPIOs 15, 27, 23 
L_DIR = 15      # Moteur branché en X, mais déplace en Y
R_DIR = 27      # Moteur branché en Y, déplace en Y
VITESSE_X = 0.0005
VITESSE_Y = 0.0004

GPIO.setmode(GPIO.BCM)         # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)        # Ne pas tenir comte des alertes
GPIO.setup(L_STEP, GPIO.OUT)     # GPIO STEP configuré en sortie
GPIO.setup(L_DIR, GPIO.OUT)      # GPIO DIR configuré en sortie
GPIO.setup(R_STEP, GPIO.OUT)
GPIO.setup(R_DIR, GPIO.OUT)

def moveX(step, direction):
    """
    Function to move in X axe (RIGHT to LEFT), with step and direction

    Parameters:
    step (int): Number of steps to move.
    direction (str): Direction to move ("cw" for clockwise, "ccw" for counter-clockwise).

    Raises:
    ValueError: If step is not a non-negative integer or direction is not "cw" or "ccw".
    
    Example of use:
    moveZ(400, "cw") or "ccw"
    """
    
    if not isinstance(step, int) or step < 0:
        raise ValueError("Step must be a non-negative integer.")
    if direction not in ["cw", "ccw"]:
        raise ValueError('Direction must be "cw" or "ccw".')

def moveY(step, direction):
    """
    Function to move in Y axis (UP/DOWN), with step and direction

    Parameters:
    step (int): Number of steps to move.
    direction (str): Direction to move ("cw" for clockwise, "ccw" for counter-clockwise).

    Raises:
    ValueError: If step is not a non-negative integer or direction is not "cw" or "ccw".

    Example of use:
    moveY(400, "cw") or "ccw"
    """
    
    if not isinstance(step, int) or step < 0:
        raise ValueError("Step must be a non-negative integer.")
    if direction not in ["cw", "ccw"]:
        raise ValueError('Direction must be "cw" or "ccw".')

    try:
        dir_state = GPIO.HIGH if direction == "cw" else GPIO.LOW
        GPIO.output(R_DIR, dir_state)
        GPIO.output(L_DIR, dir_state)

        for _ in range(step):
            GPIO.output(R_STEP, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(R_STEP, GPIO.LOW)
            sleep(VITESSE_Y)
            
            GPIO.output(L_STEP, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(L_STEP, GPIO.LOW)
            sleep(VITESSE_Y)
        

    except Exception as e:
        print(f"An error occurred: {e}")


# Garder le programme en exécution pour écouter les événements de clavier
print("Appuyez sur les flèches haut et bas pour déplacer le moteur. Appuyez sur 'q' pour quitter.")
while True:
    if keyboard.is_pressed("q"):
        print("Quitter le programme.")
        GPIO.cleanup()
        break
	
    if keyboard.is_pressed("up"):
        moveY(20, "cw")
    if keyboard.is_pressed("down"):
        moveY(20, "ccw")

    if keyboard.is_pressed("left"):
        moveX(20, "cw")	
    if keyboard.is_pressed("right"):
        moveX(20, "ccw")
