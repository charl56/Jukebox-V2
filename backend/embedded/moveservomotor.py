import RPi.GPIO as GPIO
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

try:
    while True:
        # Déplacer le servomoteur à différents angles
        moveZToAngle(0)
        time.sleep(0.2)
        moveZToAngle(90)
        time.sleep(0.2)
        moveZToAngle(180)
        time.sleep(0.2)
        moveZToAngle(90)
        time.sleep(0.2)

except KeyboardInterrupt:
    # Arrêter le PWM proprement lors de l'interruption du programme
    pwm.stop()
    GPIO.cleanup()
