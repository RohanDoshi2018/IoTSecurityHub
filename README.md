# IoTSecurityHub

### Installation

pip install paramiko

brew install zmap
open /usr/local/etc/zmap/blacklist.conf
Comment out lines for:
	10.0.0.0/8          # RFC1918: Private-Use   
	172.16.0.0/12       # RFC1918: Private-Use  
	192.168.0.0/16      # RFC1918: Private-Use  

### How to run?
####To run, past the following in bash:

export FLASK_APP=server.py
flask run

