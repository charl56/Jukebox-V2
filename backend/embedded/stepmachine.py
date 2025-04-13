#!/usr/bin/python3
# from movestepmotor import moveX, moveXToEnd, moveXToOrigin, moveY, moveYToEnd, moveYToOrigin
# from moveservomotor import moveZToAngle
# from electromagnet import electro_magnet_on, electro_magnet_off
import threading
import time

class JukeboxStateMachine:
    def __init__(self):
        self.states = ["Init", "GoToOrigin", "GoToEnd", "GoToPos", "Wait", "CalculCoords", "Close", "Play", "Pause", "Stop"]
        self.current_state = "Init"
        self.next_state = None
        self.maxStepX = 0
        self.maxStepY = 0
        self.nextCD = None
        # Movements
        self.positionFirst = None
        # Coord of each positions
        self.locationsPos = []
        for _ in range(10):
            self.locationsPos.append({'x': 0, 'y': 0})
        # Angle of Z, with servo motor
        self.locationZ = [0, 180]
        # Player actions
        self.playerActions = ["play", "pause", "stop"]
        self.actualPlayerAction = "stop"
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
        with self.lock:
            self.current_state = state
            self.state_complete_event.clear()  # Clear the event when a new state is set

    def transition(self):
        while self.stepMachineActive:
            with self.lock:
                if self.current_state == "Init":
                    print(f"{self.prefix} : Initializing...")
                    self.current_state = "GoToOrigin"

                elif self.current_state == "GoToOrigin":
                    print(f"{self.prefix} : going to origin...")
                    ## Etre sur que la fonction est terminée avant de passer à la suite
                    # moveXToOrigin()
                    # moveYToOrigin()
                    # moveZToAngle(0)

                    # Permet de retourner à l'origine sans passer par le GoToEnd
                    if self.next_state:
                        self.current_state = self.next_state
                        self.next_state = None
                    else:
                        self.current_state = "GoToEnd"

                elif self.current_state == "GoToEnd":
                    print(f"{self.prefix} : going to end...")
                    # self.maxStepX = moveXToEnd()
                    # self.maxStepY = moveYToEnd()

                    self.current_state = "GoToOrigin"
                    self.next_state = "CalculCoords"

                elif self.current_state == "CalculCoords":
                    print(f"{self.prefix} : Calcul of steps for each cd... Step to X : {self.maxStepX} and Step to Y : {self.maxStepY}")
                    self.calculateCoords()
                    print(f"{self.prefix} : Locations : {self.locationsPos}")
                    self.current_state = "Wait"

                elif self.current_state == "GoToPos":
                    print(f"{self.prefix} : Go from origin to position {self.positionFirst}")

                    ## Move X and Y to the first position
                    # moveX(self.positionFirst['x'], "cw")
                    # moveY(self.positionFirst['y'], "cw")

                    ## Move forward electromagnet
                    # moveZToAngle(self.locationZ[0])

                    ## Simulate moving
                    # time.sleep(0.1)

                    self.current_state = "Wait"

                elif self.current_state == "Play":
                    ## Start player rotation

                    print(f"{self.prefix} : Playing CD")
                    # time.sleep(0.1)
                    self.current_state = "Wait"

                elif self.current_state == "Pause":
                    print(f"{self.prefix} : Pausing CD {self.nextCD}...")
                    # time.sleep(0.1)
                    self.current_state = "Wait"

                elif self.current_state == "Stop":
                    print(f"{self.prefix} : Stopping CD...")
                    # time.sleep(0.1)
                    self.current_state = "Wait"

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
        self.locationsPos[0]['x'] = 00
        self.locationsPos[0]['y'] = 00

        self.locationsPos[1]['x'] = 11
        self.locationsPos[1]['y'] = 11
        self.locationsPos[2]['x'] = 22
        self.locationsPos[2]['y'] = 22
        self.locationsPos[3]['x'] = 33
        self.locationsPos[3]['y'] = 33

        self.locationsPos[4]['x'] = 44
        self.locationsPos[4]['y'] = 44
        self.locationsPos[5]['x'] = 55
        self.locationsPos[5]['y'] = 55
        self.locationsPos[6]['x'] = 66
        self.locationsPos[6]['y'] = 66

        self.locationsPos[7]['x'] = 77
        self.locationsPos[7]['y'] = 77
        self.locationsPos[8]['x'] = 88
        self.locationsPos[8]['y'] = 88
        self.locationsPos[9]['x'] = 99
        self.locationsPos[9]['y'] = 99


