import os

# Determine environment
IS_ON_SERVER = os.getenv("IS_ON_SERVER", "False") == "True"
IS_ON_RASPBERRY = os.getenv("IS_ON_RASPBERRY", "False") == "True"

print(f"IS_ON_SERVER: {IS_ON_SERVER} | IS_ON_RASPBERRY: {IS_ON_RASPBERRY}")


# Pins of limit switches 
SWITCH_1 = 16
SWITCH_2 = 26
SWITCH_3 = 20
SWITCH_4 = 21

# Step motor GPIOs step pins, connected to GPIOs 14, 17, 24
L_STEP = 14     # Motor plug in X, but move Y axe
R_STEP = 17     # Motor plug in Y, move Y axe

# GPIOs direction pins, connected to GPIOs 15, 27, 23
L_DIR = 15      # Motor plug in X, but move Y axe
R_DIR = 27      # Motor plug in Y, move Y axe

# Sleep time between steps for motor speed control
SLEEP_TIME = 0.002  # Adjust this value to control speed


# GPIO pin for the servo motor
SERVO_MOTOR = 18

# Electro magnet GPIO pin connected to the electromagnet
ELECTRO_MAGNET = 26