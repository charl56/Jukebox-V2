#!/usr/bin/python3
import threading
from time import sleep
import os
from embedded.config import IS_ON_RASPBERRY, IS_ON_SERVER, NB_POSITIONS, PLAYER_POSITION
from utils import load_json_file, save_json_file
import shutil


if(IS_ON_RASPBERRY):
    from embedded.movestepmotor import moveX, moveXToOrigin, moveXToEnd, moveY, moveYToOrigin, moveYToEnd
    from embedded.moveservomotor import moveZToAngle, moveZToOrigin
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
        self.actualStepZ = 0
        self.nextCD = None
        self.cdOnMagnet = False
        self.cdInPlayer = False
        self.actualCdId = 0
        # Movements
        self.positionFirst = None
        # Coord of each positions
        self.locationsPos = []
        for i in range(NB_POSITIONS):
            self.locationsPos.append({'id': str(i + 1), 'x': 0, 'y': 0, 'origin': 0, 'player': 0, 'cd': 0})
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

    def get_player_position(self):
        return self.locationsPos[PLAYER_POSITION]

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

                        if not os.path.exists("./static/positions.json"):
                            shutil.copy("./static/positions_empty.json", "./static/positions.json")

                        data = load_json_file("./static/positions.json")


                        if(len(data) == NB_POSITIONS):
                            self.locationsPos = data
                        elif(len(data) < NB_POSITIONS):
                            print(f"{self.prefix} : Not enough positions in JSON. Expected {NB_POSITIONS}, got {len(data)}. Using default positions.")
                            data.extend([{'id': str(i + 1), 'x': 0, 'y': 0, 'origin': 0, 'player': 0, 'cd': 0} for i in range(len(data), NB_POSITIONS)])
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
                        if isinstance(self.locationsPos[PLAYER_POSITION].get('origin'), int):
                            moveZToAngle(self.locationsPos[PLAYER_POSITION]['origin'])
                        else:
                            moveZToOrigin()
                    
                        self.actualStepX = 0
                        self.actualStepY = 0
                        self.actualStepZ = 0

                    # Permet de retourner à l'origine sans passer par le GoToEnd
                    if self.next_state:
                        self._set_state_locked(self.next_state)
                        self.next_state = "Wait"
                    else:
                        self._set_state_locked("Wait")
                    print("Waiting for next command...")


                elif self.current_state == "GoToEnd":
                    print(f"{self.prefix} : going to end...")

                    if(IS_ON_RASPBERRY):
                        self.maxStepX = moveXToEnd()
                        self.maxStepY = moveYToEnd()

                    self._set_state_locked("GoToOrigin")

                elif self.current_state == "GoToPos":
                    if(self.next_state == "GoToPos"): self.next_state = "Wait"

                    print(f"{self.prefix} : Go from origin to position {self.positionFirst}")
                    
                    ## Move X and Y to the first position
                    if(IS_ON_RASPBERRY):

                        directionX = ""
                        stepsX = 0
                        directionY = ""
                        stepsY = 0

                        if self.actualStepX < self.positionFirst['x']:
                            directionX = "ccw"
                            stepsX = self.positionFirst['x'] - self.actualStepX
                        else:
                            directionX = "cw"
                            stepsX = self.actualStepX - self.positionFirst['x']

                        if self.actualStepY < self.positionFirst['y']:
                            directionY = "ccw"
                            stepsY = self.positionFirst['y'] - self.actualStepY
                        else:
                            directionY = "cw"
                            stepsY = self.actualStepY - self.positionFirst['y']

                        if directionX == "ccw": self.actualStepX += moveX(stepsX, directionX)
                        else: self.actualStepX -= moveX(stepsX, directionX)

                        if directionY == "ccw": self.actualStepY += moveY(stepsY, directionY)
                        else: self.actualStepY -= moveY(stepsY, directionY)

                        # Position XY ok
                        sleep(0.5)

                        if(not self.cdOnMagnet):
                            ## Move down electromagnet
                            if self.cdInPlayer: 
                                moveZToAngle(self.locationsPos[PLAYER_POSITION]['player'])
                                print("move z to player " + self.locationsPos[PLAYER_POSITION]['player'])
                            else:
                                moveZToAngle(self.locationsPos[PLAYER_POSITION]['cd'])
                                print("move z to cd " + self.locationsPos[PLAYER_POSITION]['cd'])
                            sleep(1)
                            setMagnetOn()
                            self.cdOnMagnet = True
                            sleep(1)
                            moveZToAngle(self.locationsPos[PLAYER_POSITION]['origin'])
                            print("move z to origin " + self.locationsPos[PLAYER_POSITION]['origin'])
                        
                        else:
                            ## Move down electromagnet
                            if self.cdInPlayer: 
                                moveZToAngle(self.locationsPos[PLAYER_POSITION]['cd'])
                                print("move z to cd " + self.locationsPos[PLAYER_POSITION]['cd'])
                            else:
                                moveZToAngle(self.locationsPos[PLAYER_POSITION]['player'])
                                print("move z to player " + self.locationsPos[PLAYER_POSITION]['player'])
                            sleep(1)
                            # moveZToSupport()
                            setMagnetOff()
                            self.cdOnMagnet = False
                            # moveZToOrigin()
                            sleep(1)
                            moveZToAngle(self.locationsPos[PLAYER_POSITION]['origin'])
                            print("move z to origin " + self.locationsPos[PLAYER_POSITION]['origin'])


                    if self.next_state == None:
                        self._set_state_locked("Wait")
                        print("Waiting for next command...")
                    else:
                        self._set_state_locked(self.next_state)
                        self.next_state = None



                elif self.current_state == "Play":
                    ## Start player rotation
                    print(f"{self.prefix} : Playing CD")

                    if(IS_ON_RASPBERRY):
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        sleep(0.5)
                        GPIO.output(LED_PIN, GPIO.LOW)

                    self._set_state_locked("Wait")
                    print("Waiting for next command...")

                    # self._set_state_locked("GoToOrigin")
                    # self.next_state = "Wait"

                elif self.current_state == "Pause":
                    print(f"{self.prefix} : Pausing CD {self.nextCD}...")
                    # time.sleep(0.1)
                    self._set_state_locked("Wait")
                    print("Waiting for next command...")

                    
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
                    self.next_state = None
                    self.state_complete_event.set()  # Signal that the state is complete

                elif self.current_state == "Close":
                    print(f"{self.prefix} : Closing the machine...")
                    self.stepMachineActive = False
                    self.should_sleep = False
        
            if self.should_sleep:
                sleep(self.wait_time)


    
    def getPositions(self):
        return self.locationsPos

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

    def saveZPosition(self, positionType):
        if positionType not in ["origin", "cd", "player"]:
            print(f"{self.prefix} : Invalid Z position '{positionType}'. Must be 'origin', 'cd', or 'player'.")
            return


        for i in range(len(self.locationsPos)):
            if 'origin' not in self.locationsPos[i]:
                self.locationsPos[i]['origin'] = 0
            if 'player' not in self.locationsPos[i]:
                self.locationsPos[i]['player'] = 0
            if 'cd' not in self.locationsPos[i]:
                self.locationsPos[i]['cd'] = 0
        
            self.locationsPos[i][positionType] = self.actualStepZ


        print(f"{self.prefix} : Z position '{positionType}' saved with angle: {self.actualStepZ}")

        save_json_file("./static/positions.json", self.locationsPos)  # Save to JSON file

