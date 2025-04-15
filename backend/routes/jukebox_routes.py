# routes/jukebox_routes.py
from flask import Blueprint, jsonify
from jukebox import jukebox
import time

jukebox_bp = Blueprint('jukebox', __name__)

@jukebox_bp.route('/play/<cd_position>', methods=['POST'])
def music_play(cd_position):
    try:
        jukebox.play_cd(int(cd_position))
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/pause', methods=['POST'])
def music_pause():
    try:
        jukebox.set_state("Pause")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
    
@jukebox_bp.route('/prev', methods=['POST'])
def music_prev():
    try:
        # jukebox.set_state("Prev")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@jukebox_bp.route('/next', methods=['POST'])
def music_next():
    try:
        # jukebox.set_state("Next")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@jukebox_bp.route('/sound_update/<sound_value>', methods=['POST'])
def sound_update(sound_value):
    try:
        print("Sound value:", sound_value)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
