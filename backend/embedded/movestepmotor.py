from embedded.config import L_STEP, L_DIR, R_STEP, R_DIR, SLEEP_TIME, SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4, STEP_RETURN
import RPi.GPIO as GPIO
from time import sleep
from embedded.utils import getRealValueOfSwitch3

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

    stepMoved = 0

    try:
        dir_state = GPIO.HIGH if direction == "cw" else GPIO.LOW
        GPIO.output([R_DIR, L_DIR], dir_state)

        for _ in range(step):
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)

            stepMoved += 1

            if GPIO.input(SWITCH_1) == 0 and direction == "cw":
                print("Limite de course atteinte en X (origine)")
                moveX(STEP_RETURN, "ccw")
                stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint
                break
            elif getRealValueOfSwitch3(GPIO.input(SWITCH_3)) == 0 and direction == "ccw":
                print("Limite de course atteinte en X (fin)")
                moveX(STEP_RETURN, "cw")
                stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint
                break
        
        sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return stepMoved


def moveXToOrigin():
    """
    Function to move in X axe to the origin of the rail
    """

    try:
        GPIO.output([R_DIR, L_DIR], GPIO.HIGH)
        print("Déplacement à l'origine en X")
        
        while GPIO.input(SWITCH_1):	
            
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)

        # Comme on est à l'ogine, on peut réinitialiser le compteur de pas à 0
        # Et on recule de X pas pour avoir une petite marge
        moveX(STEP_RETURN, "ccw")
        print("Arrivé à l'origine en X")
        

    except Exception as e:
        print(f"An error occurred: {e}")


def moveXToEnd():
    """
    Function to move in X axe to the end of the rail
    
    Return: Number of steps to reach the end of the rail
    """

    stepMoved = 0
    try:
        GPIO.output([R_DIR, L_DIR], GPIO.LOW)
        print("Déplacement au max en X")
        
        while getRealValueOfSwitch3(GPIO.input(SWITCH_3)):	
            
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
            
            stepMoved += 1
        
        # Comme on est à l'ogine, on peut réinitialiser le compteur de pas à 0
        # Et on recule de X pas pour avoir une petite marge
        moveX(STEP_RETURN, "cw")
        stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return stepMoved

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
    
    stepMoved = 0

    try:
        dir_state = GPIO.HIGH if direction == "cw" else GPIO.LOW
        GPIO.output(R_DIR, not dir_state)
        GPIO.output(L_DIR, dir_state)

        for _ in range(step):
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
            stepMoved += 1

            if GPIO.input(SWITCH_2) == 0 and direction == "cw":
                print("Limite de course atteinte en Y (origine)")
                moveY(STEP_RETURN, "ccw")
                stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint
                break
            elif GPIO.input(SWITCH_4) == 0 and direction == "ccw":
                print("Limite de course atteinte en Y (fin)")
                moveY(STEP_RETURN, "cw")
                stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint
                break
        
        sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return stepMoved

def moveYToOrigin():
    """
    Function to move in Y axe to the origin of the rail
    """
    try:
        GPIO.output(R_DIR, GPIO.LOW)
        GPIO.output(L_DIR, GPIO.HIGH)
        print("Déplacement à l'origine en Y")
        
        while GPIO.input(SWITCH_2):	
            
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)

        # Comme on est à l'ogine, on peut réinitialiser le compteur de pas à 0
        # Et on monte de X pas pour avoir une petite marge
        moveY(STEP_RETURN, "ccw")
        print("Arrivé à l'origine en Y")
        

    except Exception as e:
        print(f"An error occurred: {e}")


def moveYToEnd():
    """
    Function to move in Y axe to the end of the rail
    
    Return: Number of steps to reach the end of the rail
    """
    stepMoved = 0
    try:
        GPIO.output(R_DIR, GPIO.HIGH)
        GPIO.output(L_DIR, GPIO.LOW)
        print("Déplacement au max en Y")
        
        while GPIO.input(SWITCH_4):	
            
            GPIO.output([L_STEP, R_STEP], GPIO.HIGH)
            sleep(SLEEP_TIME)
            GPIO.output([L_STEP, R_STEP], GPIO.LOW)
            sleep(SLEEP_TIME)
            
            stepMoved += 1

        # Comme on est à l'ogine, on peut réinitialiser le compteur de pas à 0
        # Et on recule de X pas pour avoir une petite marge
        moveY(STEP_RETURN, "cw")
        stepMoved -= STEP_RETURN  # On decremente les pas fait dans l'autre sens, une fois le bout atteint
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return stepMoved




