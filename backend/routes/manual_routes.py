# routes/jukebox_routes.py
from flask import Blueprint, jsonify, request
import time
from embedded.config import IS_ON_RASPBERRY

if IS_ON_RASPBERRY:
    from embedded import movestepmotor
    from embedded import moveservomotor
    from embedded import electromagnet
    from jukebox import jukebox


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

    
        if not IS_ON_RASPBERRY:
            return jsonify({"success": False, "error": "Not running on Raspberry Pi"}), 400


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

        elif(axis == "Z" and direction in ["cw", "ccw"]):
            if(direction == "cw" and jukebox.state_machine.actualStepZ - 5 >= 0):
                jukebox.state_machine.actualStepZ -= 5
            elif(direction == "cw" and jukebox.state_machine.actualStepZ - 5 < 0):
                jukebox.state_machine.actualStepZ = 0

            elif(direction == "ccw" and jukebox.state_machine.actualStepZ + 5 <= 180):
                jukebox.state_machine.actualStepZ += 5
            elif(direction == "ccw" and jukebox.state_machine.actualStepZ + 5 > 180):
                jukebox.state_machine.actualStepZ = 180
            
            print("Moving Z to angle:", jukebox.state_machine.actualStepZ)
            moveservomotor.moveZToAngle(jukebox.state_machine.actualStepZ)

        
        elif(axis == "MAGNET" and direction in ["True", "False"]):
            if(bool(direction)): electromagnet.setMagnetOn()
            else: electromagnet.setMagnetOff()
        
        else:
            return jsonify({"success": False, "error": "Invalid axis or direction"}), 400

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@manual_bp.route('/command_position', methods=['POST'])
def setPosition():
    try:

        if not IS_ON_RASPBERRY:
            return jsonify({"success": False, "error": "Not running on Raspberry Pi"}), 400


        if 'positionId' in request.json:
            positionId = request.json.get('positionId')
            positions = jukebox.saveThisPosition(positionId)
        elif 'positionType' in request.json:
            positionType = request.json.get('positionType')
            jukebox.state_machine.saveZPosition(positionType)
            positions = jukebox.getPositions()
        elif 'action' in request.json:
            jukebox.setState("GoToOrigin")
        

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
