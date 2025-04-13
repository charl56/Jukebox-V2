# routes/jukebox_routes.py
from flask import Blueprint, jsonify
from jukebox import jukebox
import time

jukebox_bp = Blueprint('jukebox', __name__)

@jukebox_bp.route('/play/<cd_position>', methods=['POST'])
def play_this_cd(cd_position):
    try:
        time.sleep(0.1)  # Simulate a delay for the CD to be inserted
        jukebox.play_cd(int(cd_position))
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/pause', methods=['POST'])
def pause_music():
    try:
        jukebox.set_state("Pause")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
