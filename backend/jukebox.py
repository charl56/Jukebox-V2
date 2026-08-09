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
        # TODO gestion de prise ou pose de cd
        self.actual_cd = cd_position
        self.state_machine.positionFirst = self.state_machine.locationsPos[cd_position]
        self.set_state("GoToPos")
        self.set_state("Play")

    def getPositions(self):
        return self.state_machine.getPositions()

    def saveThisPosition(self, positionId):
        self.state_machine.saveThisPosition(positionId)
        return self.state_machine.getPositions()

jukebox = Jukebox()