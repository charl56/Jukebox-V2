from config import STEPX_MOVE_Y, DIRX_MOVE_Y, STEPY_MOVE_Y, DIRY_MOVE_Y, STEPZ_MOVE_X, DIRZ_MOVE_X, SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4
import RPi.GPIO as GPIO
from time import sleep

VITESSE_X = 0.0005                  # Vitesse optimale rotation moteurs
VITESSE_Y = 0.0004	                # Vitesse optimale rotation moteurs

GPIO.setmode(GPIO.BCM)              # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)             # Ne pas tenir comte des alertes
GPIO.setup(STEPX_MOVE_Y, GPIO.OUT)  # GPIO STEP configuré en sortie
GPIO.setup(DIRX_MOVE_Y, GPIO.OUT)   # GPIO DIR configuré en sortie
GPIO.setup(STEPY_MOVE_Y, GPIO.OUT)
GPIO.setup(DIRY_MOVE_Y, GPIO.OUT)
GPIO.setup(STEPZ_MOVE_X, GPIO.OUT)
GPIO.setup(DIRZ_MOVE_X, GPIO.OUT)
GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# rupteurs de fin de courses
GPIO.setup(SWITCH_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

    try:
        GPIO.output(DIRZ_MOVE_X, GPIO.HIGH if direction == "cw" else GPIO.LOW)
        
        for _ in range(step):
            GPIO.output(STEPZ_MOVE_X, GPIO.HIGH)
            sleep(VITESSE_X)
            GPIO.output(STEPZ_MOVE_X, GPIO.LOW)
            sleep(VITESSE_X)	
        sleep(0.1)
    
    except Exception as e:
        print(f"An error occurred: {e}")

def moveXToEnd():
    """
    Function to move in X axe to the end of the rail
    
    Return: Number of steps to reach the end of the rail
    """
    try:
        # Initialise les variables
        stepToEndX = 0
        GPIO.output(DIRZ_MOVE_X, GPIO.LOW)
        print("Déplacement au max en X")
        
        while GPIO.input(SWITCH_1):	
            
            GPIO.output(STEPZ_MOVE_X, GPIO.HIGH)
            sleep(VITESSE_X)
            GPIO.output(STEPZ_MOVE_X, GPIO.LOW)
            sleep(VITESSE_X)
            
            stepToEndX += 1
        
        return stepToEndX
    
    except Exception as e:
        print(f"An error occurred: {e}")

def moveXToOrigin():
    """
    Function to move in X axe to the origin of the rail
    """
    try:
        # Initialise les variables
        GPIO.output(DIRZ_MOVE_X, GPIO.HIGH)
        print("Déplacement au min en X")
        
        while GPIO.input(SWITCH_2):	
            GPIO.output(STEPZ_MOVE_X, GPIO.HIGH)
            sleep(VITESSE_X)
            GPIO.output(STEPZ_MOVE_X, GPIO.LOW)
            sleep(VITESSE_X)
            
    
    except Exception as e:
        print(f"An error occurred: {e}")

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
        GPIO.output(DIRY_MOVE_Y, dir_state)
        GPIO.output(DIRX_MOVE_Y, dir_state)

        for _ in range(step):
            GPIO.output(STEPY_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPY_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
            
            GPIO.output(STEPX_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPX_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
        
        sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

def moveYToEnd():
    """
    Function to move in Y axe to the end of the rail
    
    Return: Number of steps to reach the end of the rail
    """
    try:
        # Initialise les variables
        stepToEndY = 0
        GPIO.output(DIRY_MOVE_Y, GPIO.HIGH)
        GPIO.output(DIRX_MOVE_Y, GPIO.HIGH)
        print("Déplacement au max en Y")
        
        while GPIO.input(SWITCH_3):	
            
            GPIO.output(STEPY_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPY_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
            GPIO.output(STEPX_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPX_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
            
            stepToEndY += 1
        
        return stepToEndY
    
    except Exception as e:
        print(f"An error occurred: {e}")

def moveYToOrigin():
    """
    Function to move in Y axe to the origin of the rail
    """
    try:
        # Initialise les variables
        GPIO.output(DIRY_MOVE_Y, GPIO.LOW)
        GPIO.output(DIRX_MOVE_Y, GPIO.LOW)
        print("Déplacement au min en Y")
        
        while GPIO.input(SWITCH_4):	
            GPIO.output(STEPY_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPY_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
            GPIO.output(STEPX_MOVE_Y, GPIO.HIGH)
            sleep(VITESSE_Y)
            GPIO.output(STEPX_MOVE_Y, GPIO.LOW)
            sleep(VITESSE_Y)
    
    except Exception as e:
        print(f"An error occurred: {e}")

