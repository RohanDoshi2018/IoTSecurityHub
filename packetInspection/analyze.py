#==============================================================================
# SPRING 2016 JUNIOR INDEPENDENT WORK
#title           : analyze.py
#description     : This program has two functions that can be called. 
#                : analyze_all() analyzes all the .pcap files in a 
#                : specified directory for plaintext sensitive information.
#                : Additionally, the function analyze(filename, dict) can 
#                : be called to analyze a single file and return the results
#                : in a dictionary {"ip address", : ["string1", "string2"]}
#                :
#author          : Daniel Wood
#advisor         : Nick Feamster
#date            : May 5, 2017
#usage           :python analyze.py
#==============================================================================


#!/usr/local/bin/python2.7

import dpkt
import sys
import shannon
import json
import chisqr
import glob
import socket
import os

def format(line):
  line = line.replace("\'", "")
  line = line.replace("\"", "")
  line = line.replace("\n", "")
  line = line.replace("\r", "")
  string = ""
  for c in line:
    if (ord(c) < 127 and c.isspace() == False and ord(c) > 31):
      string += c
  return string

def analyze(filename, ipdata):
  dictionary = "data/pif.txt"
  with open(dictionary) as file:
    lines = file.readlines()

  lines = [line.rstrip('\n') for line in open(dictionary)]

  counter=0
  ipcounter=0
  tcpcounter=0
  udpcounter=0
  f = open(filename,'r')
  pcap = dpkt.pcap.Reader(f)

  sha = []
  chi = []
  asc = []

  payloads=[]

  for ts, pkt in pcap:
      if counter > 2000:
        return ipdata
      counter+=1
      eth=dpkt.ethernet.Ethernet(pkt) 
      if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
         continue

      ip=eth.data
      ipcounter+=1
      ipaddr = str(socket.inet_ntoa(ip.src))
      tcp = ip.data

      if not hasattr(eth, 'ip'):
        continue
      else: 
        if not ipdata.has_key(ipaddr):
          payload=[]
          ipdata[ipaddr] = payload
        # includes TCP, TLSv1.2, HTTP, DNS, MDNS (only from 172.24.1.77), QUIC
        # LLMNR, DB-LSP-DI, udp
        if hasattr(tcp, 'dport'):
          if tcp.dport == 80 and len(tcp.data) > 0:
            ret = shannon.shannon(tcp.data)
            ret2 = chisqr.chisqr(tcp.data)

            # ascii test
            if (ret[1] < 128):
              asc.append(tcp.data)
              
            # shannon entropy test
            if (ret[0] < 6):
              sha.append(tcp.data)

              # search for word in dictionary
              for word in lines:
                if word in tcp.data:
                  string = format(tcp.data)
                  if ipdata.has_key(ipaddr):
                    if word not in ipdata[ipaddr]: 
                      ipdata[ipaddr].append(word)
                  else:
                    payload=[]
                    payload.append(word)
                    ipdata[ipaddr] = payload

            # chi squared test
            if (ret2 > 1500):
              chi.append(tcp.data)
              # print counter, ret2

          # examine packets not on port 443 or 80 with nonzero payloads
          if (tcp.dport != 443 and tcp.dport != 80 and len(tcp.data) > 0):
            ret = shannon.shannon(tcp.data)
            ret2 = chisqr.chisqr(tcp.data)

            # ascii test
            if (ret[1] < 128):
              asc.append(tcp.data)
              

            # shannon entropy test
            if (ret[0] < 6):
              sha.append(tcp.data)

              # search for word in dictionary
              for word in lines:
                if word in tcp.data:
                  string = format(tcp.data)
                  if ipdata.has_key(ipaddr):
                    if word not in ipdata[ipaddr]: 
                      ipdata[ipaddr].append(word)
                  else:
                    payload=[]
                    payload.append(word)
                    ipdata[ipaddr] = payload

            # chi squared test
            if (ret2 > 1500):
              chi.append(tcp.data)         
              # print counter, ret2

      # count the number of TCP packets
      if ip.p==dpkt.ip.IP_PROTO_TCP: 
         tcpcounter+=1

      # count the number of UDP packets
      if ip.p==dpkt.ip.IP_PROTO_UDP:
         udpcounter+=1

  # return a dictionary of {"ip address", : ["string1", "string2"]}
  f.close()
  return ipdata

def analyze_all():
  ipdata={}
  # filenames = glob.glob('../data/*.pcap')
  filenames = ["data/bpm_wlan_03.pcap", "data/sample.pcap"]
  for filename in filenames:
    #print "***************************** " + filename + " *******************************"
    ipdata = analyze(filename, ipdata)
  return ipdata

# ipdata = analyze_all()
# print ipdata

