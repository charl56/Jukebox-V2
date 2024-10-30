#!/usr/bin/python3             
# Pour executer le prog en ligne de commande
from time import sleep         # Importer la bibliotheque de gestion du temps 
import RPi.GPIO as GPIO        # Importer la bibliotheque de gestion des GPIO

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
# Pin de la pompe et de la vanne, pour la ventouse
POMPE = 10
ELECTROVANNE = 11

GPIO.setmode(GPIO.BCM)         # Paramétrage de la numérotation des GPIO en mode BCM
GPIO.setwarnings(False)        # Ne pas tenir comte des alertes
GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STEPX, GPIO.OUT)     # GPIO STEP configuré en sortie
GPIO.setup(DIRX, GPIO.OUT)      # GPIO DIR configuré en sortie
GPIO.setup(STEPY, GPIO.OUT)
GPIO.setup(DIRY, GPIO.OUT)
GPIO.setup(STEPZ, GPIO.OUT)
GPIO.setup(DIRZ, GPIO.OUT)
GPIO.setup(POMPE, GPIO.OUT)
GPIO.setup(ELECTROVANNE, GPIO.OUT)

# Fonction pour se déplacer en X, avec step et dir
def moveX(step, direction):	# moveX(400, "cw") or "ccw"
	for i in range(step):
		if(direction == "cw"):
			GPIO.output(DIRY, GPIO.HIGH)
		else:
			GPIO.output(DIRY, GPIO.LOW)
		GPIO.output(STEPY, GPIO.HIGH)
		sleep(vitesse)
		GPIO.output(STEPY, GPIO.LOW)
		sleep(vitesse)
		if(direction == "cw"):
			GPIO.output(DIRX, GPIO.HIGH)
		else:
			GPIO.output(DIRX, GPIO.LOW)
		GPIO.output(STEPX, GPIO.HIGH)
		sleep(vitesse)
		GPIO.output(STEPX, GPIO.LOW)
		sleep(vitesse)	
	sleep(1)
		
			
# Fonction pour se déplacer en Y, avec step et dir
def moveY(step, direction):	# moveY(400, "cw") or "ccw"
	for i in range(step):
		if(direction == "cw"):
			GPIO.output(DIRY, GPIO.HIGH)
		else:
			GPIO.output(DIRY, GPIO.LOW)
		GPIO.output(STEPY, GPIO.HIGH)
		sleep(vitesse)
		GPIO.output(STEPY, GPIO.LOW)
		sleep(vitesse)
		if(direction == "cw"):
			GPIO.output(DIRX, GPIO.LOW)
		else:
			GPIO.output(DIRX, GPIO.HIGH)
		GPIO.output(STEPX, GPIO.HIGH)
		sleep(vitesse)
		GPIO.output(STEPX, GPIO.LOW)
		sleep(vitesse)		
	sleep(1)


# Fonction pour se déplacer en Z, ventouse avance/recule, avec step et dir
def moveZ(step, direction):	# moveZ(400, "cw") or "ccw"
	for i in range(step):
		if(direction == "cw"):
			GPIO.output(DIRZ, GPIO.HIGH)
		else:
			GPIO.output(DIRZ, GPIO.LOW)
		GPIO.output(STEPZ, GPIO.HIGH)
		sleep(vitesse)
		GPIO.output(STEPZ, GPIO.LOW)
		sleep(vitesse)	
	sleep(1)


def diff2Coord(coord1, coord2):
	response = {'step': 0, 'direction': ''}
	
	if(coord1 == coord2):
		response['direction'] = 'cw'
		return response
		
	elif(coord1 > coord2):
		diff = coord1 - coord2
		response['step'] = diff
		response['direction'] = 'ccw'
		return response
		
	else:
		diff = coord2-coord1
		response['step'] = diff
		response['direction'] = 'cw'
		return response

def suction(status):
	if(status == 'On'):			# Activer la ventouse
		GPIO.output(POMPE, GPIO.HIGH) 			# Active la pompe
		sleep(2)								# Créer du vide pendant 2s
		GPIO.output(ELECTROVANNE, GPIO.HIGH)	# Active la vanne pour bloquer le vide
		sleep(1)
		# tester si pompe 'On' tout le temps ou pas besoin
		
	else:	# Desactiver la ventouse
		GPIO.output(ELECTROVANNE, GPIO.LOW)	# Ouvre la vanne pour laisser passer l'air
		GPIO.output(POMPE, GPIO.LOW) 			# Desactive la pompe

