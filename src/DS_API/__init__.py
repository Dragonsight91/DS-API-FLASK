from flask import Flask, redirect, render_template
from . import api

def create_app():
    app = Flask(__name__) 
    
    app.register_blueprint(api.bp)
    return app