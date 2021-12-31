# main.py

from waitress import serve
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import os
import plugins

configx = ConfigParser()
config = configx.read('config.ini')
db_enabled = None

def generate_string(length=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

if not config:
    print('No config.ini found')
    exit()

if configx.get('mysqldatabase','enabled') == 'true':
    db_enabled = True
    db_host = configx.get('mysqldatabase','host')
    db_port = configx.get('mysqldatabase','port')
    db_user = configx.get('mysqldatabase','username')
    db_pass = configx.get('mysqldatabase','password')
    db_name = configx.get('mysqldatabase','database')
    prefix = configx.get('mysqldatabase','prefix')
    db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

else:
    db_enabled = False
    db_uri = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
host = configx.get('app','host')
port = int(configx.get('app','port'))
plloaded = 0

if configx.get('app', 'secret_key') == 'random' or configx.get('app', 'secret_key') == '':
    secret = generate_string(16)
    configx.set('app', 'secret_key', secret)
else:
    secret = configx.get('app', 'secret_key')
app.config['SECRET_KEY'] = secret

@app.route('/')
def index():
    return "It works!"

if __name__ == '__main__':
    print("\nPLUGIN LOADER:")
    for i in plugins.getPlugins():
        disabled = [e.strip() for e in configx.get("plugins", "disabled").split(',')]
        if i["name"] in disabled:
            print(" > Not loading " + i["name"] + " as it is disabled in config.ini")
            continue
        else:
            print(" > Loading plugin " + i["name"])
            plugin = plugins.loadPlugin(i)
            plugin.run(app, db, configx)
            plloaded += 1
    print("\nLoaded {} plugins".format(plloaded))
    print("HOST: {}".format(host))
    print("PORT: {}".format(port))
    serve(app, host=host, port=port)