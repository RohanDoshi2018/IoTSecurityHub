#found in /usr/local/sbin/

#import getpass
import socket
import sys
import telnetlib
import paramiko
import subprocess
from subprocess import call
from subprocess import Popen, PIPE, STDOUT
import json
from paramiko.ssh_exception import AuthenticationException
import time
import string
import random
from itertools import izip

def changePassword(ip, user, password):
	#newPass = 'hello1234'

	# generate a random password
	N = 12
	newPass = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))
	print "random: "+ newPass

	# establish ssh connection
	# COMMENTED OUT FOR TESTING
	# ssh = paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# try:
	# 	# log onto device
	# 	ssh.connect(ip, username=user, password=password)
	# 	# change the password of the device
	# 	stdin, stdout, stderr = ssh.exec_command("passwd")
	# 	stdin.write(password+'\n')
	# 	stdin.write(newPass+'\n')
	# 	stdin.write(newPass+'\n')
	# 	stdin.flush()

	# 	print "try"
	# except AuthenticationException:
	# 	print "exception 1"
		#continue
	return newPass

def main():
	
	IPrange1 = "10.0.0.0/8" # private-use
	IPrange2 = "172.16.0.0/12" # private-use
	IPrange3 = "192.168.0.0/16" # private-use
	#IPrange = "172.24.1.0/24"

	ports = open('ports.txt', 'r') # testing with only 22 or 23 on there
	userpass = open('defuserpass.txt', 'r') # actual file
	#userpass = open('testpass.txt', 'r') # for testing
	successes = open('success.txt', 'w')
	deviceList = []

	# construct a dictionary with functions (case/switch)
	def ssh(ip):
		#for all IP addresses found on network:
		for line in userpass:
			# parse device info
			y = line.split('\t')
			user = y[0].strip()
			passw = y[1].strip()

			# try to establish ssh connection using default username password combination
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				ssh.connect(ip, username=user, password=passw)
				#print "try"
			except AuthenticationException:
				obj_json = {u"IPaddress": ip, u"port":22, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}
				deviceList.append(obj_json)
				#print "exception here"
				continue

			# save info about devices with default username and password 	
			successes.write(ip + '\t' + user + '\t' + passw.strip() + '\t' + '22' + '\n')
			successes.close()

			devices = open('success.txt', 'r')

			# go through all devices with default username and password
			for device in devices:
				# parse the info about the device
				x = device.split('\t')
				correctIP = x[0]
				correctUsr = x[1]
				correctPass = x[2]

				newPass = changePassword(correctIP, correctUsr, correctPass)
				obj_json = {u"IPaddress":ip, u"port":22, u"defaultUsr":user, u"defaultPass":passw, u"newPass":newPass}
				deviceList.append(obj_json)
				#print(json.dumps(obj_json))

			devices.close()

	def telnet(ip):
		HOST = ip
		#for ip in IPaddresses:
		for line in userpass:
			# parse device info
			y = line.split('\t')
			user = y[0].strip()
			password = y[1].strip()

			# try to establish a telnet connection using a default username password combination
			p = Popen(["telnet", "-l", user, HOST],stdin=PIPE,stdout=PIPE,stderr=PIPE)

			response = ""
			while not "Password: " in response:
				response += p.stdout.read(1)

			p.stdin.write(password + '\n')
			p.stdin.flush()

			time.sleep(4)
			response = p.stdout.readline()
			# try next username password combination if this one did not work
			if "Login incorrect" in response:
				obj_json = {u"IPaddress":ip, u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}
				deviceList.append(obj_json)
				continue
			# save info about devices with default username and password 	
			else:
				successes.write(ip + '\t' + user + '\t' + password.strip() + '\t' + '23' + '\n')
				successes.close()

			devices = open('success.txt', 'r')

			# go through all devices with default username and password
			for device in devices:
				# parse device information
				x = device.split('\t')
				correctIP = x[0]
				correctUsr = x[1]
				correctPass = x[2]

				newPass = changePassword(correctIP, correctUsr, correctPass)
				obj_json = {u"IPaddress":ip, u"port":23, u"defaultUsr":user, u"defaultPass":password, u"newPass":newPass}
				deviceList.append(obj_json)
				#print(json.dumps(obj_json))

			devices.close()

	options = {22 : ssh,
				23 : telnet,
	}

	for p in ports:
		# call bash command to run ZMap on the network
		# writes out the IP addresses on the network to a file
		subprocess.call(["./zmap", "-p", p, "-o", "IPaddresses1.txt", IPrange1, "--max-sendto-failures", "17000000"])
		subprocess.call(["./zmap", "-p", p, "-o", "IPaddresses2.txt", IPrange2, "--max-sendto-failures", "1000000"])
		subprocess.call(["./zmap", "-p", p, "-o", "IPaddresses3.txt", IPrange3, "--max-sendto-failures", "1000000"])

		# concatenate the 3 textfiles created
		filenames = ['IPaddresses1.txt', 'IPaddresses2.txt', 'IPaddresses3.txt']
		with open('IPaddresses.txt', 'w') as outfile:
			for fname in filenames:
				with open(fname) as infile:
					outfile.write(infile.read())

		# go throught the IP addresses found on the network
		IPaddresses = open('IPaddresses.txt', 'r')
		for ip in IPaddresses:
			# for ssh port:
			if p == '22':
				options[22](ip.strip())
			# for telnet port:
			if p == '23':
				options[23](ip.strip())

	# call dumps on the whole list of all devices
	#open a file and write out
	#with open('devices.txt', 'w') as outputfile:
	#	outputfile.write(json.dumps(deviceList))
	print json.dumps(deviceList)


	IPaddresses.close()
	ports.close()
	userpass.close()
	successes.close()
	#outputfile.close()

main()

