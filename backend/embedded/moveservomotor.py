from config import SERVO_MOTOR
import RPi.GPIO as GPIO
import time

# Configuration du mode de numérotation des pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_MOTOR, GPIO.OUT)

# Initialisation du signal PWM à 50Hz
pwm = GPIO.PWM(SERVO_MOTOR, 50)  # Fréquence de 50Hz
pwm.start(0)  # Démarrer le PWM avec un cycle de service de 0

def moveZToAngle(angle):
    """
    Function to move in Z axe to an angle between 0 and 180 degrees

    Parameters:
    angle (int): Angle to move the servo motor to (between 0 and 180 degrees).

    Raises:
    ValueError: If angle is not between 0 and 180 degrees.
    
    Example of use:
    moveZToAngle(90)
    """
    duty = 2 + (angle / 18)  # Calcul du cycle de service correspondant à l'angle
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.2)  # Temps pour laisser le servomoteur atteindre la position
    pwm.ChangeDutyCycle(0)
