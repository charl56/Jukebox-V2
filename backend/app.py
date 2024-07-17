import json
import threading 
from flask_cors import CORS
from flask import Flask, jsonify, request, render_template, send_from_directory
import time
import os
import subprocess
from embedded.stepmachine import JukeboxStateMachine
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


actual_cd = 0
jukebox = JukeboxStateMachine()

# Index app
@app.route('/')
def index():
   return render_template('index.html')
# Assets files
@app.route('/assets/<path:filename>', methods=['GET'])
def serve_static(filename):
   return send_from_directory('templates/assets', filename)


# Pictures to front
@app.route('/images/<path:filename>', methods=['GET'])
def return_image(filename):
   return send_from_directory('static/', filename)

###
### Gestion des données, affichage
###
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
      with open('./static/data.json', 'w', encoding='utf-8') as file:
         json.dump(data, file, ensure_ascii=True)

      # Send results back as a json
      resp = {"success": True}
      return jsonify(resp), 200 
   
   except Exception as e:
      return "error: " + str(e)

# Upload albums image
@app.route('/upload', methods=['POST'])
def upload_file():
   if 'file' not in request.files or 'fileName' not in request.form:
      return 'No file or picture name part',  400

   file = request.files['file']
   picture_name = request.form['fileName']
   
   if file.filename == '':
      return 'No selected file',  400
   
   # Sauvegardez le fichier avec le nom donné
   file.save(os.path.join('./static/albums/', picture_name))
   return 200

###
### Action pour intéragir avec la jukebox
###
# Route pour ajouter un cd sur le lecteur
@app.route('/playThisCd', methods=['POST'])
def playThisCd():
   try:
      # data from front
      data = str(request.json['data'])

      global actual_cd
      if actual_cd != 0:

         print("Remove cd to ", actual_cd)
         time.sleep(1)

      # Save position of new cd
      actual_cd = data
      print("Play this CD : ", data)
      jukebox.nextCD = data
      jukebox.set_state("Play")
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
      jukebox.set_state("Play")
      
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
      jukebox.set_state("Pause")
      
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
      global actual_cd
      actual_cd = 0
      # Permet de simuler la pose du cd
      time.sleep(1)
      jukebox.set_state("Stop")
      
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

   jukebox_thread = threading.Thread(target=jukebox.transition)
   jukebox_thread.daemon = True
   jukebox_thread.start()


   # Adresse ip pour lancer en local
   app.run(host='127.0.0.1', port=5025, debug=True, use_reloader=False)