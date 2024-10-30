# app.py
import threading
from flask import Flask
from flask_cors import CORS
from routes.main_routes import main_bp
from routes.data_routes import data_bp
from routes.jukebox_routes import jukebox_bp
from jukebox import jukebox

DEBUG = True
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(main_bp)
app.register_blueprint(data_bp)
app.register_blueprint(jukebox_bp)

if __name__ == '__main__':
   jukebox_thread = threading.Thread(target=jukebox.transition)
   jukebox_thread.daemon = True
   jukebox_thread.start()

   app.run(host='127.0.0.1', port=5025, debug=True, use_reloader=False)