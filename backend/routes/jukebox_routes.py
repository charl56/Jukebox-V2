# routes/jukebox_routes.py
from flask import Blueprint, jsonify, request
from jukebox import jukebox
import time

jukebox_bp = Blueprint('jukebox', __name__)

@jukebox_bp.route('/play/<cdPosition>', methods=['POST'])
def play_this_cd(cdPosition):
    try:
        print(cdPosition)
        time.sleep(1)  # Simulate a delay for the CD to be inserted
        # cd_position = int(request.json['data'])
        # jukebox.play_cd(cd_position)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/pause', methods=['POST'])
def pause_music():
    try:
        print("pause")
        # jukebox.set_state("Pause")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
