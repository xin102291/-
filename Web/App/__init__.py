from flask import Flask
from App.route import *

def create_app(app):
    # app = Flask(__name__,static_folder="static", static_url_path="/")
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login)
    app.add_url_rule('/homepage', 'homepage', homepage)
    app.add_url_rule('/dashboard', 'dashboard', dashboard)
    app.add_url_rule('/health', 'health', health)
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/signup', 'signup', signup)
    return app

