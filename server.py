from __future__ import print_function
from flask import Flask, request, url_for, redirect, render_template, session
import os, sys
from DefaultPasswordProtection import defaultpass
from packetInspection import analyze

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

@app.route('update')
def update():
	IP_to_Device = {
		'172.24.1.81':'WeMo Smart Switches',
		'172.24.1.107':'YI Home Camera',
		'172.24.1.63':'Android Phone Interface With Blood Pressure Monitor'
	}

	# Gudrun
	password_results = [{"IPaddress": '172.24.1.107', "port": 22, "defaultUsr": 'root', "defaulsPass": 'admin', "newPass": 'k4Txp02IqmVe'}]
	# password_results = defaultpass.check_passwords()

	# Daniel
	sensitive_info = {'172.24.1.107': ["Daniel", "Blood Pressure", "ID = 123456"] }	
	sensitive_info = analyze.analyze()

	# Rohan
	# TODO

	render_template('index.html')