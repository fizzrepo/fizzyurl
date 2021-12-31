from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import os, plugins

configx = ConfigParser()
config = configx.read('config.ini')
db_enabled = None

if not config:
    print('No config.ini found')
    exit()

if configx.get('mysqldatabase','enabled') == 'true':
    db_enabled = True
    db_host = config["mysqldatabase"]["host"]
    db_port = config["mysqldatabase"]["port"]
    db_user = config["mysqldatabase"]["username"]
    db_pass = config["mysqldatabase"]["password"]
    db_name = config["mysqldatabase"]["database"]
    prefix = config["mysqldatabase"]["prefix"]
    db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)

else:
    db_enabled = False
    db_uri = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "It works!"

if __name__ == '__main__':
    for i in plugins.getPlugins():
        print("Loading plugin " + i["name"])
        plugin = plugins.loadPlugin(i)
        plugin.run(app)
    app.run(debug=True)