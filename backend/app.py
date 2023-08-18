import json 
from flask_cors import CORS
from flask import Flask, jsonify, request, render_template
import time
import subprocess

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


####

# # App
# @app.route('/')
# def index():
#     return render_template('index.html')

# Route envoyer les données au front
@app.route('/getData', methods=['GET'])
def getData():
   try:
      # Opening JSON file
      data = open('./static/data.json')
      
      # returns JSON object as a dictionary
      dataLoad = json.load(data)

      # Send results back as a json
      resp = {"success": True, "data": dataLoad}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)

# Route pour syncroniser les données de l'app dans le back (POST)
@app.route('/syncData', methods=['POST'])
def syncData():
   try:
      # data from front
      data = str(request.json['data'])

      # Ouvrir le fichier JSON en mode écriture
      with open('./static/data.json', 'w') as file:
         json.dump(data, file, ensure_ascii=False)

      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)
   

# Route pour ajouter un cd sur le lecteur
@app.route('/playThisCd', methods=['POST'])
def playThisCd():
   try:
      # data from front
      data = str(request.json['data'])

      print("Play this CD : ", data)
      # Permet de simuler la pose du cd
      time.sleep(1)
      
      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)
   
# Route pour mettre play sur le cd en place
@app.route('/playMusic', methods=['POST'])
def playMusic():
   try:

      print("player start : ")
      # Permet de simuler la pose du cd
      time.sleep(1)
      
      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)

# Route pour mettre en pause le cd en place
@app.route('/pauseMusic', methods=['POST'])
def pauseMusic():
   try:

      print("player pause")
      # Permet de simuler la pose du cd
      time.sleep(1)
      
      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)


# Route enlever le cd en place
@app.route('/removeFromPlayer', methods=['POST'])
def removeFromPlayer():
   try:

      print("Remove CD ")
      # Permet de simuler la pose du cd
      time.sleep(1)
      
      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)


if __name__ == '__main__':

   # path_frontend = '../frontend/'
   # commande_npm = 'npm run build'

   # try:
   #    subprocess.run(commande_npm, shell=True, cwd=path_frontend, check=True)
   #    print("Frontend build ready !")
   # except subprocess.CalledProcessError as e:
   #    print("Error build frontend:", e)

   # Adresse ip pour lancer en local
   app.run(host='127.0.0.1', port=5025, debug=True)