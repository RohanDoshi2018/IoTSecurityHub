from __future__ import print_function
from flask import Flask, request, url_for, redirect, render_template, session
import os, sys
from DefaultPasswordProtection import defaultpass
from packetInspection import analyze
import json

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

@app.route('/update')
def update():
	ip_to_name = {
		'172.24.1.81':'WeMo Smart Switches',
		'172.24.1.107':'YI Home Camera',
		'172.24.1.63':'Android Phone Interface With Blood Pressure Monitor'
	}

	# Gudrun
	password_results = {
		'172.24.1.81':  {"port": 22, "defaultUsr": 'root', "defaulsPass": 'admin', "newPass": '2372jhkxdfxf'}, 
		'172.24.1.107':  {"port": 22, "defaultUsr": 'admin', "defaulsPass": 'pass', "newPass": 'k4Txp02IqmVe'}, 
		'172.24.1.63':  {"port": 22, "defaultUsr": 'user', "defaulsPass": 'pass', "newPass": 'vcx46666n334'} 
	}

	# Daniel
	sensitive_data_leak_results = {'172.24.1.81': ["Daniel", "Blood Pressure", "ID = 123456"], '172.24.1.107': [], '172.24.1.63' : []}

	# Rohan 
	attack_results = {'172.24.1.81': False, '172.24.1.107': True, '172.24.1.63' : True}

	devices = []
	for ip, name in ip_to_name.items():
		device = {}
		device['ip'] = ip
		device['name'] = name

		if password_results[ip]['newPass'] != None:
			device['is_password_insecure'] = True
			device['newPass'] = password_results[ip]['newPass'] 			
		else: 
			device['is_password_insecure'] = False


		if len(sensitive_data_leak_results[ip]) > 0:
			device['is_sensitive_info'] = True
			device['sensitive_info'] = sensitive_data_leak_results[ip]			
		else: 
			device['is_sensitive_info'] = False

		device['is_attack'] =  attack_results[ip]

		devices.append(device)

	return render_template('index.html', devices=devices)

# devices = [
# 	{
# 		'ip': '172.24.1.81',
# 		'name': 'WeMo Smart Switch',
# 		'is_password_insecure': True,
# 		'is_sensitive_info': True,
# 		'is_attack': True,
# 		'newPass': 'k4Txp02IqmVe',
# 		'sensitive_info': ["Daniel", "Blood Pressure", "ID = 123456"]
# 	}, 
# 	{
# 		'ip': '172.24.1.107',
# 		'name': 'YI Home Camera',
# 		'is_password_insecure': False,
# 		'is_sensitive_info': False,
# 		'is_attack': True
# 	}, 	
# 	{
# 		'ip': '172.24.1.63',
# 		'name': 'Android Phone Interface With Blood Pressure Monitor',
# 		'is_password_insecure': True,
# 		'is_sensitive_info': True,
# 		'is_attack': True,
# 		'newPass': '15hjh3535235',
# 		'sensitive_info': ["John", "California", "City = San Fransisco"]
# 	} 
# ]
