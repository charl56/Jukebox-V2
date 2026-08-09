#!/usr/bin/python3
import threading
import time
import os
from embedded.config import IS_ON_RASPBERRY, NB_POSITIONS
from utils import load_json_file, save_json_file


if(IS_ON_RASPBERRY):
    from embedded.movestepmotor import moveX, moveXToOrigin, moveXToEnd, moveY, moveYToOrigin, moveYToEnd
    from embedded.moveservomotor import moveZToAngle, moveZToOrigin, moveZToPlayer, moveZToSupport
    from embedded.electromagnet import setMagnetOn, setMagnetOff
    
    import RPi.GPIO as GPIO

    LED_PIN = 18  # Vous pouvez changer ce numéro selon votre connexion
    GPIO.setmode(GPIO.BCM)  # Utilisation de la numérotation BCM
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)  # LED éteinte au démarrage
    
    


def cleanup():
    GPIO.cleanup()
# Gestionnaire pour exécuter le nettoyage à la fermeture
import atexit
atexit.register(cleanup)


class JukeboxStateMachine:
    def __init__(self):
        self.states = ["Init", "GoToOrigin", "GoToEnd", "GoToPos", "Wait", "CalculCoords", "Close", "Play", "Pause", "Prev", "Next"]
        self.current_state = "Init"
        self.next_state = None
        self.maxStepX = 0
        self.maxStepY = 0
        self.actualStepX = 0
        self.actualStepY = 0
        self.nextCD = None
        self.cdOnMagnet = False
        # Movements
        self.positionFirst = None
        # Coord of each positions
        self.locationsPos = []
        for i in range(NB_POSITIONS):
            self.locationsPos.append({'id': str(i + 1), 'x': 0, 'y': 0})
        # Angle of Z, with servo motor
        self.locationZ = [0, 180]
        # Player actions
        self.playerActions = ["play", "pause"]
        self.actualPlayerAction = ""
        self.stepMachineActive = True
        # Thread
        self.lock = threading.Lock()
        self.wait_time = 1
        self.should_sleep = True
        # Prefix print
        self.prefix = "StateMachine"
        # Event for state completion
        self.state_complete_event = threading.Event()


    def get_state(self):
        with self.lock:
            return self.current_state

    def set_state(self, state):
        """Appelé depuis l'extérieur du thread transition() — acquiert le lock."""
        with self.lock:
            self._set_state_locked(state)

    def _set_state_locked(self, state):
        """Appelé depuis transition(), qui tient déjà le lock."""
        self.current_state = state
        self.state_complete_event.clear()


    def transition(self):
        while self.stepMachineActive:
            with self.lock:
                if self.current_state == "Init":
                    print(f"{self.prefix} : Initializing...")
             
                    try:
                        data = load_json_file("./static/positions.json")
                        if(len(data) == NB_POSITIONS):
                            self.locationsPos = data
                        elif(len(data) < NB_POSITIONS):
                            print(f"{self.prefix} : Not enough positions in JSON. Expected {NB_POSITIONS}, got {len(data)}. Using default positions.")
                            data.extend([{'id': str(i + 1), 'x': 0, 'y': 0} for i in range(len(data), NB_POSITIONS)])
                            self.locationsPos = data
                            save_json_file("./static/positions.json", self.locationsPos)
                        else:
                            raise FileNotFoundError(f"{self.prefix} : Too many positions in JSON. Expected {NB_POSITIONS}, got {len(data)}. Using default positions.")

                    except FileNotFoundError:
                        print(f"{self.prefix} : File not found, using default positions.")

                    self._set_state_locked("GoToOrigin")
                    self.next_state = "GoToEnd"


                elif self.current_state == "GoToOrigin":
                    print(f"{self.prefix} : going to origin...")
                    ## Etre sur que la fonction est terminée avant de passer à la suite
                    if(IS_ON_RASPBERRY):
                        moveXToOrigin()
                        moveYToOrigin()
                        moveZToOrigin()

                        self.actualStepX = 0
                        self.actualStepY = 0

                    # Permet de retourner à l'origine sans passer par le GoToEnd
                    if self.next_state:
                        self._set_state_locked(self.next_state)
                        self.next_state = "Wait"
                    else:
                        self._set_state_locked("Wait")

                elif self.current_state == "GoToEnd":
                    print(f"{self.prefix} : going to end...")

                    if(IS_ON_RASPBERRY):
                        self.maxStepX = moveXToEnd()
                        self.maxStepY = moveYToEnd()

                    self._set_state_locked("GoToOrigin")


                elif self.current_state == "GoToPos":
                    print(f"{self.prefix} : Go from origin to position {self.positionFirst}")

                    ## Move X and Y to the first position
                    if(IS_ON_RASPBERRY):

                        # TODO : caluler le nb de pas en fonction de la pisition actuelle (0 normalement),
                        # Et choisir en fonction cw ou ccw pour aller à la position souhaitée

                        directionX = ""
                        stepsX = 0
                        directionY = ""
                        stepsY = 0

                        if self.actualStepX < self.positionFirst['x']:
                            directionX = "ccw"
                            stepsX = self.positionFirst['x'] - self.actualStepX
                        else:
                            directionX = "cw"
                            stepsX = self.positionFirst['x'] - self.actualStepX

                        if self.actualStepY < self.positionFirst['y']:
                            directionY = "ccw"
                            stepsY = self.positionFirst['y'] - self.actualStepY
                        else:
                            directionY = "cw"
                            stepsY = self.positionFirst['y'] - self.actualStepY

                        if directionX == "ccw": self.actualStepX += moveX(stepsX, directionX)
                        else: self.actualStepX -= moveX(stepsX, directionX)

                        if directionY == "ccw": self.actualStepY += moveY(stepsY, directionY)
                        else: self.actualStepY -= moveY(stepsY, directionY)



                        if(not self.cdOnMagnet):
                            ## Move down electromagnet
                            moveZToPlayer()
                            setMagnetOn()
                            self.cdOnMagnet = True
                            moveZToOrigin()
                        
                        else:
                            ## Move down electromagnet
                            moveZToSupport()
                            setMagnetOff()
                            self.cdOnMagnet = False
                            moveZToOrigin()


                    self._set_state_locked("GoToOrigin")

                elif self.current_state == "Play":
                    ## Start player rotation
                    print(f"{self.prefix} : Playing CD")

                    if(IS_ON_RASPBERRY):
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        time.sleep(1)
                        GPIO.output(LED_PIN, GPIO.LOW)

                    self._set_state_locked("GoToOrigin")
                    self.next_state = "Wait"

                elif self.current_state == "Pause":
                    print(f"{self.prefix} : Pausing CD {self.nextCD}...")
                    # time.sleep(0.1)
                    self._set_state_locked("Wait")
                    
                elif self.current_state == "Prev":
                    print(f"{self.prefix} Prev sound...")
                    # time.sleep(0.1)
                    self._set_state_locked("Wait")

                elif self.current_state == "Next":
                    print(f"{self.prefix} Next sound...")
                    # time.sleep(0.1)
                    self._set_state_locked("Wait")

                elif self.current_state == "Wait":
                    # Instead of sleeping inside the lock, release it and sleep outside
                    self.should_sleep = True
                    self.state_complete_event.set()  # Signal that the state is complete

                elif self.current_state == "Close":
                    print(f"{self.prefix} : Closing the machine...")
                    self.stepMachineActive = False
                    self.should_sleep = False
        
            if self.should_sleep:
                time.sleep(self.wait_time)


    def calculateCoords(self):

        ## Origin, permet ensuite d'avoir le cd n°1 dans la liste self.locationsPos[1]...
        # self.locationsPos[0]['x'] = 00
        # self.locationsPos[0]['y'] = 00
        print("Not used")
        # self.locationsPos[1]['x'] = 11
        # self.locationsPos[1]['y'] = 11
        
        # self.locationsPos[2]['x'] = 22
        # self.locationsPos[2]['y'] = 22
        
        # self.locationsPos[3]['x'] = 33
        # self.locationsPos[3]['y'] = 33

    def saveThisPosition(self, position):
        try:
            position = int(position) - 1
        except (ValueError, TypeError):
            print(f"{self.prefix} : Position invalide '{position}', doit être un entier.")
            return

        print(f"Saving position... {position} with coordinates: ({self.actualStepX}, {self.actualStepY})")
        if position < 0 or position >= len(self.locationsPos) + 1:
            print(f"{self.prefix} : Invalid position {position}. Must be between 0 and {len(self.locationsPos)-1}.")
            return

        self.locationsPos[position]['x'] = self.actualStepX
        self.locationsPos[position]['y'] = self.actualStepY
        print(f"{self.prefix} : Position {position} saved with coordinates: ({self.actualStepX}, {self.actualStepY})")

        save_json_file("./static/positions.json", self.locationsPos)  # Save to JSON file

    def getPositions(self):
        return self.locationsPos
