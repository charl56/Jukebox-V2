# jukebox.py
from embedded.stepmachine import JukeboxStateMachine

class Jukebox:
    def __init__(self):
        self.state_machine = JukeboxStateMachine()
        self.actual_cd = 0

    def transition(self):
        self.state_machine.transition()

    def set_state(self, state):
        self.state_machine.set_state(state)
        self.state_machine.state_complete_event.wait()

    def play_cd(self, cd_position):
        if self.actual_cd != 0:
            self.remove_cd()

        self.actual_cd = cd_position
        self.state_machine.positionFirst = self.state_machine.locationsPos[cd_position]
        self.state_machine.positionSecond = self.state_machine.locationsPos[5]  # 5 is the player
        self.set_state("GoToPos")
        self.set_state("Play")

    def remove_cd(self):
        self.state_machine.positionFirst = self.state_machine.locationsPos[5]
        self.state_machine.positionSecond = self.state_machine.locationsPos[self.actual_cd]
        self.set_state("GoToPos")
        self.actual_cd = 0

jukebox = Jukebox()