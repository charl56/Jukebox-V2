from config import L_STEP, L_DIR, R_STEP, R_DIR, SLEEP_TIME, SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4
import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)              # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)             # Ne pas tenir comte des alertes
GPIO.setup([L_STEP, R_STEP, L_DIR, R_DIR], GPIO.OUT)  # GPIO STEP configuré en sortie
GPIO.setup([SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4], GPIO.IN, pull_up_down=GPIO.PUD_UP)	# rupteurs de fin de courses

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
        dir_state = GPIO.HIGH if direction == "cw" else GPIO.LOW
        GPIO.output(R_DIR, dir_state)
        GPIO.output(L_DIR, dir_state)

        for _ in range(step):
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
        
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
        GPIO.output(R_DIR, not dir_state)
        GPIO.output(L_DIR, dir_state)

        for _ in range(step):
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
        
        sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")


def moveXYToOrigin():
    """
    Function to move in Y axe to the origin of the rail
    """
    try:
        # Initialise les variables
        GPIO.output(R_DIR, GPIO.LOW)
        GPIO.output(L_DIR, GPIO.LOW)
        print("Déplacement au min en Y")
        
        while GPIO.input(SWITCH_4):	
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
def moveXYToEnd():
    """
    Function to move in Y axe to the end of the rail
    
    Return: Number of steps to reach the end of the rail
    """
    try:
        # Initialise les variables
        stepToEndY = 0
        GPIO.output(R_DIR, GPIO.HIGH)
        GPIO.output(L_DIR, GPIO.HIGH)
        print("Déplacement au max en Y")
        
        while GPIO.input(SWITCH_3):	
            
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
            
            stepToEndY += 1
        
        return stepToEndY
    
    except Exception as e:
        print(f"An error occurred: {e}")



