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
            # print counter
            # print tcp.data
            # http = dpkt.http.Request(tcp.data)
            ret = shannon.shannon(tcp.data)
            ret2 = chisqr.chisqr(tcp.data)

            # ascii test
            if (ret[1] < 128):
              asc.append(tcp.data)
              

            # shannon entropy test
            if (ret[0] < 6):
              sha.append(tcp.data)
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

          if (tcp.dport != 443 and tcp.dport != 80 and len(tcp.data) > 0):
            ret = shannon.shannon(tcp.data)
            ret2 = chisqr.chisqr(tcp.data)

            # ascii test
            if (ret[1] < 128):
              asc.append(tcp.data)
              

            # shannon entropy test
            if (ret[0] < 6):
              sha.append(tcp.data)
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

      if ip.p==dpkt.ip.IP_PROTO_TCP: 
         tcpcounter+=1

      if ip.p==dpkt.ip.IP_PROTO_UDP:
         udpcounter+=1
  return ipdata

  # print "Total number of packets in the pcap file: ", counter
  # print "Total number of ip packets: ", ipcounter
  # print "Total number of tcp packets: ", tcpcounter
  # print "Total number of udp packets: ", udpcounter

  # words1, packets1 = dictSearch.dictSearch(asc)
  # words2, packets2 = dictSearch.dictSearch(chi)
  # words3, packets3 = dictSearch.dictSearch(sha)


  # print "------------------------- ASCII ---------------------------------"
  # for word, line in zip(words2, packets2):
  #   line = format(line)
  #   print word
  #   print line
  #   print

  # print "------------------------- CHI SQUARE ------------------------------"
  # for word, line in zip(words2, packets2):
  #   line = format(line)
  #   print word
  #   print line
  #   print

  # print "------------------------- SHANNON ------------------------------"
  # for word, line in zip(words3, packets3):
  #   line = format(line)
  #   payloads.append(line)
  #   print word
  #   print line
  #   print


  # data = {}
  # data['payloads'] = payloads
  # json_data = json.dumps(data)

  # f.close()

def analyze_all():
  ipdata={}
  # filenames = glob.glob('../data/*.pcap')
  filenames = ["data/bpm_wlan_03.pcap", "data/sample.pcap"]
  for filename in filenames:
    #print "***************************** " + filename + " *******************************"
    ipdata = analyze(filename, ipdata)
  return ipdata

ipdata = analyze_all()
print ipdata

