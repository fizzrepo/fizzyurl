# main.py

import configparser
from waitress import serve
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import os
import plugins
import databasestuff
import utils
configx = ConfigParser()
config = configx.read('config.ini')
db_enabled = None

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
URL = databasestuff.setup(db)
host = configx.get('app','host')
port = int(configx.get('app','port'))
plloaded = 0
PLUGXD = []

if configx.get('app', 'secret_key') == 'random' or configx.get('app', 'secret_key') == '':
    secret = utils.generate_string(16)
    configx.set('app', 'secret_key', secret)
else:
    secret = configx.get('app', 'secret_key')
app.config['SECRET_KEY'] = secret
app.secret_key = secret

print("Loading core")

@app.route('/')
def index():
    return "Hello World!"

@app.route('/<shorturl>')
def redirect(shorturl):
    url = URL.query.filter_by(shorturl=shorturl).first()
    if url is None:
        try:
            return render_template('{}.html'.format(shorturl=shorturl))
        except:
            return "Not found"
    url.clicks += 1
    db.session.commit()
    return redirect(url.originalurl)

@app.route('/api/shorten', methods=['POST'])
def shorten():
    url = request.form['url']
    if not utils.is_valid_url(url):
        return "Invalid URL", 400
    return jsonify(utils.shorten_url(db, url, URL))

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
    db.create_all()
    print("\nLoaded {} plugins".format(plloaded))
    print("HOST: {}".format(host))
    print("PORT: {}".format(port))
    print("http://{}:{}/".format(host, port))
    serve(app, host=host, port=port)