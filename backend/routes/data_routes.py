# routes/data_routes.py
import os
from flask import Blueprint, jsonify, request
from utils import load_json_file, save_json_file

data_bp = Blueprint('data', __name__)

@data_bp.route('/cd', methods=['GET'])
def get_data():
    try:
        data = load_json_file('./static/data.json')
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@data_bp.route('/cd', methods=['POST'])
def sync_data():
    try:
        data = request.json['data']
        save_json_file('./static/data.json', data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@data_bp.route('/image', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'fileName' not in request.form:
        return jsonify({"success": False, "error": "No file or picture name part"}), 400

    file = request.files['file']
    picture_name = request.form['fileName']

    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    file.save(os.path.join('./static/albums/', picture_name))
    return jsonify({"success": True}), 200


@data_bp.route('/image/<fileName>', methods=['DELETE'])
def delete_file(fileName):

    file_path = os.path.join('./static/albums/' + fileName + '.jpg')

    if not os.path.exists(file_path):
        return jsonify({"success": False, "error": "File not found"}), 404
    
    try:
        os.remove(file_path)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True}), 200