#found in /usr/local/sbin/

#import getpass
import socket
import sys
import telnetlib
import paramiko
import subprocess
from subprocess import call, check_output
from subprocess import Popen, PIPE, STDOUT
import json
from paramiko.ssh_exception import AuthenticationException, SSHException
import time
import string
import random
from itertools import izip

def changePassword(ip, port, user, password):
	#newPass = 'hello1234'

	# generate a random password
	N = 12
	newPass = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))
	#print "random: "+ newPass

	#establish ssh connection
	#COMMENTED OUT FOR TESTING
	if port == 22:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			# log onto device
			ssh.connect(ip, username=user, password=password)
			# change the password of the device
			stdin, stdout, stderr = ssh.exec_command("passwd")
			stdin.write(password+'\n')
			stdin.write(newPass+'\n')
			stdin.write(newPass+'\n')
			stdin.flush()
			#print "try"
			return newPass
		except AuthenticationException:
			print "exception 1"
			return 0
			#continue
	# elif port == 23:
	# 	# try to establish a telnet connection using a default username password combination
	# 	p = Popen(["telnet", "-l", user, ip],stdin=PIPE,stdout=PIPE,stderr=PIPE)
	
	# 	response = ""
	# 	while not "Password: " in response:
	# 		response += p.stdout.read(1)

	# 	p.stdin.write(password + '\n')
	# 	p.stdin.flush()

	# 	time.sleep(4)
	# 	response = p.stdout.readline()
	# 	# try next username password combination if this one did not work
	# 	#if "Login incorrect" in response:
	# 	if "login" in response:
	# 		#obj_json = {u"IPaddress":ip, u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}
	# 		obj_json = {ip:{u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
	# 		deviceList.append(obj_json)
	# 		#continue
	# 	# save info about devices with default username and password 	
	# 	else:
	# 		# log onto device
	# 		#ssh.connect(ip, username=user, password=password)
	# 		# change the password of the device
	# 		#stdin, stdout, stderr = p.exec_command("passwd")
	# 		#p = Popen(["passwd"])
	# 		#p.stdin.write("passwd"+'\n')
	# 		#time.sleep(4)
	# 		print "password:" + newPass
	# 		pp = Popen(["echo", "hello"],stdin=PIPE,stdout=PIPE,stderr=PIPE) #p.stdin.write(password+'\n')
	# 		p.stdin.write(newPass+'\n')
	# 		p.stdin.write(newPass+'\n')
	# 		p.stdin.flush()
	# 		#print "try"
	# 		return newPass

def main():
	
	#IPrange1 = "10.0.0.0/8" # private-use
	#IPrange = "172.16.0.0/12" # private-use
	#IPrange3 = "192.168.0.0/16" # private-use
	#IPrange = "172.24.1.0/24" # for the Pi

	ports = open('ports.txt', 'r') # testing with only 22 or 23 on there
	#userpass = open('defuserpass.txt', 'r') # actual file
	userpass = open('testpass.txt', 'r') # for testing
	successes = open('success.txt', 'w')
	deviceList = []

	# construct a dictionary with functions (case/switch)
	def ssh(ip):
		#for all IP addresses found on network:
		success = 0
		for line in userpass:
			# parse device info
			y = line.split('\t')
			user = y[0].strip()
			passw = y[1].strip()

			# try to establish ssh connection using default username password combination
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			try:
				print "user: "+user
				print "password: "+passw
				ssh.connect(ip, username=user, password=passw)
				#print "try"
			except AuthenticationException:
				
				#obj_json = {ip:{u"port":22, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
				# dict with IP as key and value is a dictionary of the other stuff
				#deviceList.append(obj_json)
				#print "exception here"
				continue
			except SSHException:
				print "Caught an SSHException"
				continue


			time.sleep(4)

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

				newPass = changePassword(correctIP, 22, correctUsr, correctPass)
				#obj_json = {u"IPaddress":ip, u"port":22, u"defaultUsr":user, u"defaultPass":passw, u"newPass":newPass}
				if newPass != 0:
					success = 1
					obj_json = {ip:{u"port":22, u"defaultUsr":user, u"defaultPass":passw, u"newPass":newPass}}
					deviceList.append(obj_json)
				#print(json.dumps(obj_json))

			devices.close()
		if success == 0:
			obj_json = {ip:{u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
			deviceList.append(obj_json)

	def telnet(ip):
		HOST = ip
		#for ip in IPaddresses:
		success = 0
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
				#print "resp: " + response

			time.sleep(2)
			p.stdin.write(password + '\n')
			p.stdin.flush()

			time.sleep(6)
			response = p.stdout.read(19)
			# try next username password combination if this one did not work
			#print response
			if "Login incorrect" in response:
			#if "login" in response:
				#obj_json = {u"IPaddress":ip, u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}
				#obj_json = {ip:{u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
				#deviceList.append(obj_json)
				continue
			# save info about devices with default username and password 	
			else:
				success = 1
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

				newPass = changePassword(correctIP, 23, correctUsr, correctPass)
				#obj_json = {u"IPaddress":ip, u"port":23, u"defaultUsr":user, u"defaultPass":password, u"newPass":newPass}
				if newPass != 0:
					obj_json = {ip:{u"port":23, u"defaultUsr":user, u"defaultPass":password, u"newPass":newPass}}
					deviceList.append(obj_json)
				else:
					obj_json = {ip:{u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
					deviceList.append(obj_json)
				#print(json.dumps(obj_json))

			devices.close()
		if success == 0:
			obj_json = {ip:{u"port":23, u"defaultUsr":"N/A", u"defaultPass":"N/A", u"newPass":"N/A"}}
			deviceList.append(obj_json)

	options = {22 : ssh,
				23 : telnet,
	}

	for p in ports:

		inetAddress = check_output(["ifconfig", "en0", "inet"])
		#print inetAddress #string
		ipAddress = ""
		i = 0
		length = len(inetAddress)
		#print inetAddress + '\n'
		parsed = inetAddress.split()
		#print parsed[5] # IP address
		ipParsed = parsed[5].split('.')

		finalIPrange = ipParsed[0]+'.'+ipParsed[1]+'.'+ipParsed[2]+'.0/24'
		#print finalIPrange

		print "finaliprange: " + finalIPrange
		# call bash command to run ZMap on the network
		subprocess.call(["./zmap", "-p", p, "-o", "IPaddresses.txt", finalIPrange]) # for Raspberry Pi

		# go throught the IP addresses found on the network within the specified range
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

