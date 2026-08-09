# routes/jukebox_routes.py
from flask import Blueprint, jsonify, request
import time
from embedded.config import IS_ON_RASPBERRY
from jukebox import jukebox

if IS_ON_RASPBERRY:
    from embedded import movestepmotor
    from embedded import moveservomotor
    from embedded import electromagnet


manual_bp = Blueprint('manual', __name__)

@manual_bp.route('/command', methods=['POST'])
def getCommand():
    try:
        command = request.json.get('command')
            
    
        # On vérifie le contenu reçu
        parts = command.split("_")
        if(parts[0] != "MOVE" and parts[0] != "TOGGLE"):
            return jsonify({"success": False, "error": "Invalid command format"}), 400
        
        # On extrait les paramètres
        axis = parts[1]
        direction = parts[2]

    
        # if not IS_ON_RASPBERRY:
        #     return jsonify({"success": False, "error": "Not running on Raspberry Pi"}), 400


        if(axis == "X" and direction in ["cw", "ccw"]):
            steps = movestepmotor.moveX(50, direction) 
            if(direction == "cw"):
                jukebox.state_machine.actualStepX -= steps
            else:
                jukebox.state_machine.actualStepX += steps

        elif(axis == "Y" and direction in ["cw", "ccw"]):
            steps = movestepmotor.moveY(50, direction)
            if(direction == "cw"):
                jukebox.state_machine.actualStepY -= steps
            else:
                jukebox.state_machine.actualStepY += steps

        elif(axis == "Z" and int(direction) <= 180 and int(direction) >= 0):
            moveservomotor.moveZToAngle(int(direction))
        
        elif(axis == "MAGNET" and direction in ["True", "False"]):
            if(bool(direction)): electromagnet.setMagnetOn()
            else: electromagnet.setMagnetOff()
        
        else:
            return jsonify({"success": False, "error": "Invalid axis or direction"}), 400

        return jsonify({"success": True, "stepX": stepX, "stepY": stepY}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@manual_bp.route('/command_position', methods=['POST'])
def setPosition():
    try:
        positionId = request.json.get('positionId')
        positions = jukebox.saveThisPosition(positionId)

        return jsonify({"success": True, "positions": positions}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@manual_bp.route('/command_position', methods=['GET'])
def getPositions():
    try:
        print("Getting positions...")
        positions = jukebox.getPositions()
        return jsonify({"success": True, "positions": positions}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
