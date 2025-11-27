# routes/jukebox_routes.py
from flask import Blueprint, jsonify, request
import time
from embedded.config import IS_ON_RASPBERRY

if IS_ON_RASPBERRY:
    from embedded import movestepmotor

manual_bp = Blueprint('manual', __name__)

@manual_bp.route('/command', methods=['POST'])
def getCommand():
    try:
        command = request.json.get('command')
        print(command)
        
        if(command == "TOGGLE_MAGNET"):
            # machine.send("TOGGLE_MAGNET")
            print("Toggling electromagnet")
        else:
            # On vérifie le contenu reçu
            parts = command.split("_")
            if(parts[0] != "MOVE" or len(parts) != 3):
                return jsonify({"success": False, "error": "Invalid command format"}), 400
            
            # On extrait les paramètres
            axis = parts[1]
            direction = parts[2]

        
            if not IS_ON_RASPBERRY:
                return jsonify({"success": False, "error": "Not running on Raspberry Pi"}), 400
        
            if(axis == "X" and direction in ["cw", "ccw"]):
                movestepmotor.moveX(50, direction)

            elif(axis == "Y" and direction in ["cw", "ccw"]):
                movestepmotor.moveY(50, direction)
            
            else:
                return jsonify({"success": False, "error": "Invalid axis or direction"}), 400
              
        


        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

