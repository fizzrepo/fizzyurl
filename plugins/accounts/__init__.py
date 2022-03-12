import os
from configparser import ConfigParser
from flask import redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

def run(app, db, config):
    configx = ConfigParser()
    configx.read('config.ini')
    cfg = {}

    cfg["DISCORD_CLIENT_ID"] = configx.get('config', 'client_id')
    cfg["DISCORD_CLIENT_SECRET"] = configx.get('config', 'client_secret')
    cfg["DISCORD_REDIRECT_URI"] = configx.get('config', 'redirect_uri')
    
    discord = DiscordOAuth2Session(app)

    @app.route("/login")
    def login():
        return discord.create_session()

    @app.route("/callback")
    def authorized():
        discord.callback()
        return redirect(url_for(".me"))

    @app.route("/profile")
    @app.route("/profile/<id>")
    @requires_authorization
    def profile(id=None):
        user = discord.fetch_user()
        if id is None:
            id = user.id
        return "Hello, {}. You're viewing the user profile of {}.".format(user.name, id)