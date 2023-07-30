import json 
from flask_cors import CORS
from flask import Flask, jsonify, request

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


####
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



# Route pour recevoir des requetes du front (POST)
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



if __name__ == '__main__':
   # Adresse ip pour lancer en local
   app.run(host='127.0.0.1', port=5025, debug=True)