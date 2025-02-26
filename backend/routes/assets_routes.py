from flask import Blueprint, render_template, send_from_directory

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/assets/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

@assets_bp.route('/images/<path:filename>', methods=['GET'])
def return_image(filename): 
    return send_from_directory('static/', filename)