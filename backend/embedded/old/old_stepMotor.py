# -*- coding: utf-8 -*-
#!/usr/bin/python3             
# Pour executer le prog en ligne de commande
from time import sleep         # Importer la bibliotheque de gestion du temps 
import RPi.GPIO as GPIO        # Importer la bibliotheque de gestion des GPIO

from stepMotors.stepMotorMove import *


# Switchs interrupteur
SWITCH_1 = 16
SWITCH_2 = 26
SWITCH_3 = 16	# 20
SWITCH_4 = 26	# 21
# Commandes de pas, reliées aux GPIOs 14, 17, 24
STEPX = 14     # gauche   
STEPY = 17     # droite                     
STEPZ = 24     # ventouse  
# Commandes de direction, reliées aux GPIOs 15, 27, 23 
DIRX = 15      # gauche
DIRY = 27      # droite               
DIRZ = 23      # ventouse
vitesse = 0.0004	# Vitesse optimale rotation moteurs

GPIO.setmode(GPIO.BCM)         # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)        # Ne pas tenir comte des alertes
GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# rupteurs de fin de courses
GPIO.setup(SWITCH_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STEPX, GPIO.OUT)     # GPIO STEP configuré en sortie
GPIO.setup(DIRX, GPIO.OUT)      # GPIO DIR configuré en sortie
GPIO.setup(STEPY, GPIO.OUT)
GPIO.setup(DIRY, GPIO.OUT)
GPIO.setup(STEPZ, GPIO.OUT)
GPIO.setup(DIRZ, GPIO.OUT)




class StepMotorsFunctions:

	#  Import des fonction moveX et moveY : stepMotorMove
	def stateMachine(cdNumberRecieve):
		print("state machine ;:::: ",cdNumberRecieve)																
		# States
		INIT = 0
		MOVE_XY = 1
		MOVE_Z = 2
		SUCTION_CUP = 3
		GOTOEND = 4
		CALCULCOORDS = 5
		GOTOCD = 6
		
		# variables
		cdNumber = cdNumberRecieve # Position dans la liste des coordonnées du cd voulu/lecteur
		oldCdNumber = 0
		stepToEndX = 0	# Step qui vont servir pour les max a l'init
		stepToEndY = 0
		stepToEndZ = 250
		distXcm = 33	# Dimensions X et y en cm
		distYcm = 35
		stepByCmX = 0	# Nombre de step pour 1 cm en x
		stepByCmY = 0
		coordsCdslecteur = []	# Liste des coords des cd et du lecteur
		coordLectX = 0		# Coordonnées du lecteur
		coordLectY = 0
		spaceBetweenCdCm = 16	# Espace entre chaque cd, en x et y
		spaceBetweenCdStep = 0
		cdInPlayer = True	# Cd dans le lecteur
		cdOnSuction = False	# Cd dans la ventouse
		wait = False
		
		suctionNextToCd = False
		suctionAction = False
		stepPosX = 200
		stepPosY = 400
		stepsToOrigin = 3200
		stepsXtoPlayer = 20
		stepsYtoPlayer = 20
		stepToCd = 500      # Calculé à l'avance, il ne change plus après
		rotSens1 = "CW" # or "CCW", clockwise or counter clockwise
		rotSens2 = "CW" # or "CCW"
		rotSens3 = "CW" # or "CCW"
		
		
		# Pour aller plus vite
		stepToEndX = 2357
		stepToEndY = 2500
		state = CALCULCOORDS
		# Pour simuler un cd deja en place
		oldCdNumber = 2		
				
		# state = INIT
		
		while True : 
			print("Entrée machine d'état")
			### Etat d'initialisation des moteurs, les déplaces en 0;0, en bas à gauche de la jukebox
			### les moteurs s'arrêterons avant d'avoir fait les setpsTo0, si ils sont arrivés au bout : switch micro-rupteur 
			
			## INIT
			if state == INIT : 
				
				# moveXToOrigin
				# moveYToOrigin
				# moveServoToAngle(0)
    
    
				if(cdNumber == 420):
					print("Fin machine à état")
					break;
				if(coordsCdslecteur == []):
					state = GOTOEND
				else:
					state = GOTOCD
			## GO TO END	
			if state == GOTOEND : 
			
				### Go to end to know nm of steps
				# stepToEndX = moveXToEnd()
				# stepToEndY = MoveXToEnd()
				
		

				state = CALCULCOORDS
				

			## CALCUL COORDS
			if state == CALCULCOORDS : 
				
				# Calcul d'abord du nombre de step par cm
				print("Calcul de step par cm")
				stepByCmX = int(stepToEndX/distXcm)
				stepByCmY = int(stepToEndY/distYcm)
				print("--", stepByCmX, " step.cm X; ", stepByCmY, " step.cm Y")
				
				if(stepByCmX != stepByCmY): # Recommencer l'init si les valeur ne sont pas égale : verif
					print("state = init")
					state = INIT
				else :
				
					# Création liste des coordonnées des cds/lecteur : 1 = bas a gauche, 8 = haut a droite
					i = 0
					for i in range(9):
						coordsCdslecteur.append({
							'x': 0,
							'y': 0,
							'sens': "CW"})

					# Calcul des coordonnées du lecteur, le point du milieu
					coordLectX = (distXcm/2)*stepByCmX
					coordLectY = (distYcm/2)*stepByCmY
					# print("Coordonnée lecteur :", coordsCdslecteur)

					# Conversion distance entre les cd cm * step.cm = nb step
					spaceBetweenCdStep = spaceBetweenCdCm * stepByCmX
					# print("spaceBetweenCdStep :", spaceBetweenCdStep, coordLectX-spaceBetweenCdStep)

					# Remplissage du tableau des coordonnées, a optimiser
					coordsCdslecteur[0]['x'] = int(coordLectX-spaceBetweenCdStep)
					coordsCdslecteur[0]['y'] = int(coordLectY-spaceBetweenCdStep)
					coordsCdslecteur[1]['x'] = int(coordLectX)
					coordsCdslecteur[1]['y'] = int(coordLectY-spaceBetweenCdStep)
					coordsCdslecteur[2]['x'] = int(coordLectX+spaceBetweenCdStep)
					coordsCdslecteur[2]['y'] = int(coordLectY-spaceBetweenCdStep)
					
					coordsCdslecteur[3]['x'] = int(coordLectX-spaceBetweenCdStep)
					coordsCdslecteur[3]['y'] = int(coordLectY)
					coordsCdslecteur[4]['x'] = int(coordLectX)
					coordsCdslecteur[4]['y'] = int(coordLectY)
					coordsCdslecteur[5]['x'] = int(coordLectX+spaceBetweenCdStep)
					coordsCdslecteur[5]['y'] = int(coordLectY)
									
					coordsCdslecteur[6]['x'] = int(coordLectX-spaceBetweenCdStep)
					coordsCdslecteur[6]['y'] = int(coordLectY+spaceBetweenCdStep)
					coordsCdslecteur[7]['x'] = int(coordLectX)
					coordsCdslecteur[7]['y'] = int(coordLectY+spaceBetweenCdStep)						
					coordsCdslecteur[8]['x'] = int(coordLectX+spaceBetweenCdStep)
					coordsCdslecteur[8]['y'] = int(coordLectY+spaceBetweenCdStep)	
									
					print("Coordonnée lecteur :", coordsCdslecteur)
					
					state = INIT

			## GO TO CD
			if state == GOTOCD : 
				print("GOTOCD : ",cdNumber, coordsCdslecteur[4])
				
				# Si cd dans le lecteur : go player, take cd, go old cd
				if(cdInPlayer):
					print("CD enplace, changement")
					# Go to lecteur
					stepMotorMove.moveX(coordsCdslecteur[4]['x'], "cw")
					stepMotorMove.moveY(coordsCdslecteur[4]['y'], "cw")
					
					# Go in front of lecteur, take cd and go back
					print("avance devant le cd, actgive la ventouse et recule")
					stepMotorMove.moveZ(stepToEndZ, "cw")			
					stepMotorMove.suction('On')
					stepMotorMove.moveZ(stepToEndZ, "ccw")

					
					# Calcul step et dir de différence entre cdPlayer et old cd
					diffX = stepMotorMove.diff2Coord(coordsCdslecteur[4]['x'], coordsCdslecteur[oldCdNumber]['x'])
					diffY = stepMotorMove.diff2Coord(coordsCdslecteur[4]['y'], coordsCdslecteur[oldCdNumber]['y'])
					print("diffs : ", diffX, diffY)
					
					# Go to old cd pos
					stepMotorMove.moveX(diffX['step'], diffX['direction'])
					stepMotorMove.moveY(diffY['step'], diffY['direction'])
					

					# Go in front of lecteur, put cd and go back
					print("avance devant le cd, desactive la ventouse et recule")
					stepMotorMove.moveZ(stepToEndZ, "cw")			
					stepMotorMove.suction('Off')
					stepMotorMove.moveZ(stepToEndZ, "ccw")
						
					# il n'y a donc plus de CD dans le lecteur
					cdInPlayer = False
					
					# Calcul step et dir de différence entre old cd et cd demandé
					diffX = stepMotorMove.diff2Coord(coordsCdslecteur[oldCdNumber]['x'], coordsCdslecteur[int(cdNumber)]['x'])
					diffY = stepMotorMove.diff2Coord(coordsCdslecteur[oldCdNumber]['y'], coordsCdslecteur[int(cdNumber)]['y'])
					print("diffs : ", diffX, diffY)
					
					# Go to new cd pos
					stepMotorMove.moveX(diffX['step'], diffX['direction'])
					stepMotorMove.moveY(diffY['step'], diffY['direction'])
				
				
				else:	# Si pas de cd dans le player, la ventouse est à l'origine au démarrage, 
					# Go to cd voulu
					stepMotorMove.moveX(coordsCdslecteur[cdNumber]['x'], "cw")
					stepMotorMove.moveY(coordsCdslecteur[cdNumber]['y'], "cw")
				
				# Go in front of lecteur, take cd and go back
				stepMotorMove.moveZ(stepToEndZ, "cw")			
				stepMotorMove.suction('On')
				stepMotorMove.moveZ(stepToEndZ, "ccw")
				
				# Calcul step et dir de différence entre cd demandé et lecteur
				diffX = stepMotorMove.diff2Coord(coordsCdslecteur[int(cdNumber)]['x'], coordsCdslecteur[4]['x'])
				diffY = stepMotorMove.diff2Coord(coordsCdslecteur[int(cdNumber)]['y'], coordsCdslecteur[4]['y'])
				print("diffs : ", diffX, diffY)
				
				# Go to cd player
				stepMotorMove.moveX(diffX['step'], diffX['direction'])
				stepMotorMove.moveY(diffY['step'], diffY['direction'])
							
				# Go in front of lecteur, put cd and go back
				stepMotorMove.moveZ(stepToEndZ, "cw")			
				stepMotorMove.suction('Off')
				stepMotorMove.moveZ(stepToEndZ, "ccw")		
							
							
							
				# Une fois le cd voulu en plus, les coordonnées de l'ancien cd = coord du cd choisie							
				oldCdNumber = cdNumber
				cdInPlayer = True
				
				# Go to player
				cdNumber = 420	# 420 = Cd en place, on arrête la machine d'état
				state = INIT









