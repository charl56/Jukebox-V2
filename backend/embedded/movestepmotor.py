from config import STEPX_MOVE_Y, DIRX_MOVE_Y, STEPY_MOVE_Y, DIRY_MOVE_Y, STEPZ_MOVE_X, DIRZ_MOVE_X
import RPi.GPIO as GPIO
from time import sleep

vitesse = 0.001	# Mieux que 0.0005

GPIO.setmode(GPIO.BCM)         # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)        # Ne pas tenir comte des alertes
GPIO.setup(STEPX_MOVE_Y, GPIO.OUT)     # GPIO STEP configuré en sortie
GPIO.setup(DIRX_MOVE_Y, GPIO.OUT)      # GPIO DIR configuré en sortie
GPIO.setup(STEPY_MOVE_Y, GPIO.OUT)
GPIO.setup(DIRY_MOVE_Y, GPIO.OUT)
GPIO.setup(STEPZ_MOVE_X, GPIO.OUT)
GPIO.setup(DIRZ_MOVE_X, GPIO.OUT)


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
            sleep(vitesse)
            GPIO.output(STEPZ_MOVE_X, GPIO.LOW)
            sleep(vitesse)	
        sleep(0.1)
    
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
            sleep(vitesse)
            GPIO.output(STEPY_MOVE_Y, GPIO.LOW)
            sleep(vitesse)
            
            GPIO.output(STEPX_MOVE_Y, GPIO.HIGH)
            sleep(vitesse)
            GPIO.output(STEPX_MOVE_Y, GPIO.LOW)
            sleep(vitesse)
        
        sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")

      

