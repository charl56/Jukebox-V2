# routes/jukebox_routes.py
from flask import Blueprint, jsonify, request
from jukebox import jukebox

jukebox_bp = Blueprint('jukebox', __name__)

@jukebox_bp.route('/playThisCd', methods=['POST'])
def play_this_cd():
    try:
        cd_position = int(request.json['data'])
        jukebox.play_cd(cd_position)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/playMusic', methods=['POST'])
def play_music():
    try:
        jukebox.set_state("Play")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/pauseMusic', methods=['POST'])
def pause_music():
    try:
        jukebox.set_state("Pause")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@jukebox_bp.route('/removeFromPlayer', methods=['POST'])
def remove_from_player():
    try:
        jukebox.remove_cd()
        jukebox.set_state("Stop")
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500