# routes/main_routes.py
from flask import Blueprint, render_template, send_from_directory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/assets/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('templates/assets', filename)

@main_bp.route('/images/<path:filename>', methods=['GET'])
def return_image(filename): 
    return send_from_directory('static/', filename)