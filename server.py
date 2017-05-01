from __future__ import print_function
from flask import Flask, request, url_for, redirect, render_template, session
import os, sys

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True, 
    SECRET_KEY = os.urandom(24),
    UPLOAD_FOLDER = 'tmp/'
)

@app.route('/')
def index():
    return render_template('index.html')