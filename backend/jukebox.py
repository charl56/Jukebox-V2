# jukebox.py
from embedded.stepmachine import JukeboxStateMachine
from embedded.config import PLAYER_POSITION

class Jukebox:
    def __init__(self):
        self.state_machine = JukeboxStateMachine()

    def transition(self):
        self.state_machine.transition()

    def set_state(self, state):
        self.state_machine.set_state(state)
        self.state_machine.state_complete_event.wait()





    def play_cd(self, cd_position):

# Si cd poosition == position du cd dans le lecteur ou si cd position == position du lecteur
        # + 1 car on recoit un id qui commence par 1, pas 0 ; Trop chiant de convertir à différents endroits ??? 
        print("cd_position:", cd_position)
        print("actualCdId:", self.state_machine.actualCdId)
        print("PLAYER_POSITION + 1:", PLAYER_POSITION + 1)
        print("cdInPlayer:", self.state_machine.cdInPlayer)

        if self.state_machine.cdInPlayer == False:
            # On init la position de départ, le fait qu'il n'y a pas de manet pour aller chercher le CD
            self.state_machine.positionFirst = self.state_machine.locationsPos[cd_position - 1] # -1 car l'id commence a 1 et index à 0
            self.state_machine.cdOnMagnet = False
            self.set_state("GoToPos")
            # Ensuite on le dépose sur le lecteur, et retourne à l'origine
            self.state_machine.positionFirst = self.state_machine.get_player_position()
            self.state_machine.cdOnMagnet = True
            self.state_machine.next_state = "GoToOrigin"
            self.set_state("GoToPos")
            # Une fois placé on init dans la machine l'id du cd sur le lecteur
            self.state_machine.actualCdId = cd_position
            self.state_machine.cdInPlayer = True

        elif cd_position == (PLAYER_POSITION + 1) and self.state_machine.cdInPlayer == False:
            raise ValueError("Aucun CD à enlever du lecteur.")

        elif cd_position == self.state_machine.actualCdId or cd_position == (PLAYER_POSITION + 1):  
            # On déplace le rail au lecteur pour récupérer le CD
            self.state_machine.positionFirst = self.state_machine.get_player_position()
            self.state_machine.cdOnMagnet = False
            self.state_machine.next_state = "Wait"
            self.set_state("GoToPos")
            # Puis le dépose a sa place, et retourne à l'origine
            self.state_machine.positionFirst = self.state_machine.locationsPos[self.state_machine.actualCdId - 1]
            self.state_machine.cdOnMagnet = True
            self.state_machine.next_state = "GoToOrigin"
            self.set_state("GoToPos")
            # Vide variables
            self.state_machine.actualCdId = 0
            self.state_machine.cdInPlayer = False

        else:
            raise ValueError("Enlever le cd du lecteur avant d'en ajouter un nouveau")
       


    def getPositions(self):
        return self.state_machine.getPositions()

    def saveThisPosition(self, positionId):
        self.state_machine.saveThisPosition(positionId)
        return self.state_machine.getPositions()

jukebox = Jukebox()