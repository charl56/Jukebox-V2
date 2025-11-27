# app.py
import os
import threading
from flask import Flask
from flask_cors import CORS
from routes.main_routes import main_bp
from routes.data_routes import data_bp
from routes.manual_routes import manual_bp
from embedded.config import IS_ON_SERVER, IS_ON_RASPBERRY


DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(main_bp)
app.register_blueprint(data_bp, url_prefix='/api')
app.register_blueprint(manual_bp, url_prefix='/api/manual')

# Only import jukebox and start the thread if not running in Docker
if not IS_ON_SERVER:
   from jukebox import jukebox 
   from routes.jukebox_routes import jukebox_bp

   app.register_blueprint(jukebox_bp, url_prefix='/api/jukebox')

   jukebox_thread = threading.Thread(target=jukebox.transition)
   jukebox_thread.daemon = True
   jukebox_thread.start()


if __name__ == '__main__':
   if(IS_ON_SERVER or IS_ON_RASPBERRY):
      app.run(host='0.0.0.0', port=5025, use_reloader=False)
   else:
      app.run(host='127.0.0.1', port=5025, debug=True, use_reloader=False)
