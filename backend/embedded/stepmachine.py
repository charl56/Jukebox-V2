#!/usr/bin/python3
# from movestepmotor import moveX, moveXToEnd, moveXToOrigin, moveY, moveYToEnd, moveYToOrigin
# from moveservomotor import moveZToAngle
import threading
import time

class JukeboxStateMachine:
    def __init__(self):
        self.states = ["Init", "GoToOrigin", "GoToEnd", "Wait", "CalculCoords", "Close", "Play", "Pause", "Stop"]
        self.current_state = "Init"
        self.next_state = None
        self.maxStepX = 0
        self.maxStepY = 0
        self.nextCD = None
        self.previousCd = None
        self.coordGoTo = (0, 0)
        self.coordGoToAfter = (0, 0)
        self.locationsPos = []
        self.playerActions = ["play", "pause", "stop"]
        self.actualPlayerAction = "stop"
        self.stepMachineActive = True
        # Thread
        self.lock = threading.Lock()
        self.wait_time = 1
        self.should_sleep = True

    def get_state(self):
        with self.lock:
            return self.current_state
    
    def set_state(self, state):
        with self.lock:
            self.current_state = state

    def transition(self):
        while self.stepMachineActive:
            with self.lock:
                if self.current_state == "Init":
                    print("Initializing...")
                    self.current_state = "GoToOrigin"
                
                elif self.current_state == "GoToOrigin":
                    print("going to origin...")
                    ## Etre sur que la fonction est terminée avant de passer à la suite
                    # moveXToOrigin()
                    # moveYToOrigin()
                    # moveZToAngle(0)
                    
                    # Permet de retourner à l'origine sans passer par le GoToEnd
                    if self.next_state is not None:
                        self.current_state = self.next_state
                        self.next_state = None
                    else:
                        self.current_state = "GoToEnd"
                
                elif self.current_state == "GoToEnd":
                    print("going to end...")
                    # self.maxStepX = moveXToEnd()
                    # self.maxStepY = moveYToEnd()
                    
                    self.current_state = "GoToOrigin"
                    self.next_state = "CalculCoords"
                
                elif self.current_state == "CalculCoords":
                    print("Calcul of steps for each cd...")
                    self.locationsPos = self.calculateCoords()
                    self.current_state = "Wait"
                    
                elif self.current_state == "GOTOPOS":
                    print("go to this cd : ")
                    print(self.nextCD)
                    self.current_state = "Wait"
                    
                elif self.current_state == "Play":
                    print(f"Playing CD {self.nextCD}...")
                    time.sleep(3)
                    self.current_state = "Wait"
                
                elif self.current_state == "Pause":
                    print(f"Pausing CD {self.nextCD}...")
                    time.sleep(3)
                    self.current_state = "Wait"
                
                elif self.current_state == "Stop":
                    print("Stopping CD...")
                    time.sleep(3)
                    self.current_state = "Wait"                
                
                elif self.current_state == "Wait":
                    print("Waiting for action...")
                    # Instead of sleeping inside the lock, release it and sleep outside
                    self.should_sleep = True
                
                elif self.current_state == "Close":
                    print("Closing the machine...")
                    self.stepMachineActive = False
                    self.should_sleep = False

            if self.should_sleep:
                time.sleep(self.wait_time)

    def calculateCoords(self):
        locations = []
        for _ in range(9):
            locations.append({'x': 0, 'y': 0})
        
        locations[0]['x'] = 14
        locations[0]['y'] = 4525
        locations[1]['x'] = 345
        locations[1]['y'] = 534
        locations[2]['x'] = 654
        locations[2]['y'] = 45
        
        locations[3]['x'] = 111
        locations[3]['y'] = 111
        locations[4]['x'] = 111
        locations[4]['y'] = 111
        locations[5]['x'] = 111
        locations[5]['y'] = 111
                        
        locations[6]['x'] = 11
        locations[6]['y'] = 11
        locations[7]['x'] = 22
        locations[7]['y'] = 14
        locations[8]['x'] = 252
        locations[8]['y'] = 7
        
        return locations

        
        
        
    #     if self.current_state == "Init":
    #         print("Initializing...")
    #         # Example of moving to the origin
    #         self.current_state = "GoToOrigin"
        
    #     elif self.current_state == "GoToOrigin":
    #         print("Moving to origin...")
    #         self.masterStepX = 0
    #         self.masterStepY = 0
    #         self.current_state = "Wait"
        
    #     elif self.current_state == "Wait":
    #         if action is not None:
    #             print(f"Waiting for action: {action}")
    #             self.current_state = "NewAction"
        
    #     elif self.current_state == "NewAction":
    #         if action == "placer":
    #             print("Placing a CD...")
    #             self.previousCd = self.nextCD
    #             self.nextCD = None
    #             self.coordGoTo = self.coordGoToAfter
    #             self.current_state = "GoToPos"
    #         elif action == "enlever":
    #             print("Removing a CD...")
    #             self.previousCd = None
    #             self.coordGoTo = self.coordGoToAfter
    #             self.current_state = "GoToPos"
    #         elif action == "wait":
    #             print("Waiting...")
    #             self.current_state = "Wait"
        
    #     elif self.current_state == "GoToPos":
    #         print(f"Moving to position: {self.coordGoTo}")
    #         # Simulate moving to coordinates
    #         self.current_state = "Wait"
        
    #     elif self.current_state == "Play":
    #         print("Playing CD...")
    #         self.actualPlayerAction = "play"
    #         self.current_state = "Wait"
        
    #     elif self.current_state == "Pause":
    #         print("Pausing CD...")
    #         self.actualPlayerAction = "pause"
    #         self.current_state = "Wait"
        
    #     elif self.current_state == "Stop":
    #         print("Stopping CD...")
    #         self.actualPlayerAction = "stop"
    #         self.current_state = "Wait"
        
    #     else:
    #         print("Invalid state")


    # def set_action(self, action):
    #     self.transition(action)

    # def manual_mode(self):
    #     print("Entering manual mode...")
    #     # Implementation for manually moving the motors and recording steps
    #     # For demonstration purposes, this function will be simulated
    #     steps = input("Enter steps moved (e.g., 'x:10 y:20 z:30'): ")
    #     x, y, z = map(int, steps.split())
    #     print(f"Recorded steps: X={x}, Y={y}, Z={z}")
    #     self.locationsPos['new_position'] = (x, y, z)

# Example usage
# if __name__ == "__main__":
#     jukebox = JukeboxStateMachine()
#     print(f"Initial state: {jukebox.get_state()}")
#     jukebox.transition()  # Init -> GoToOrigin
#     print(f"Current state: {jukebox.get_state()}")
#     jukebox.transition()  # GoToOrigin -> Wait
#     print(f"Current state: {jukebox.get_state()}")
#     jukebox.set_action("placer")  # Wait -> NewAction
#     print(f"Current state: {jukebox.get_state()}")
#     jukebox.transition()  # NewAction -> GoToPos
#     print(f"Current state: {jukebox.get_state()}")
#     jukebox.transition()  # GoToPos -> Wait
#     print(f"Current state: {jukebox.get_state()}")
#     jukebox.manual_mode()  # Manual mode to record steps
#     print(f"Locations positions: {jukebox.locationsPos}")
