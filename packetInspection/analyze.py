#!/usr/local/bin/python2.7

import dpkt
import sys
import shannon
import dictSearch
import json
import chisqr
import glob

def format(line):
  line = line.replace("\'", "")
  line = line.replace("\"", "")
  line = line.replace("\n", "")
  line = line.replace("\r", "")
  string = ""
  for c in line:
    if (ord(c) < 128 and c.isspace() == False):
      string += c
  return string

def analyze(filename):
  counter=0
  ipcounter=0
  tcpcounter=0
  udpcounter=0

  f = open(filename,'r')
  pcap = dpkt.pcap.Reader(f)

  sha = []
  chi = []
  asc = []

  for ts, pkt in pcap:

      counter+=1
      eth=dpkt.ethernet.Ethernet(pkt) 
      if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
         continue

      ip=eth.data
      ipcounter+=1

      tcp = ip.data

      if not hasattr(eth, 'ip'):
        continue
      else: 

        # includes TCP, TLSv1.2, HTTP, DNS, MDNS (only from 172.24.1.77), QUIC
        # LLMNR, DB-LSP-DI, udp
        if hasattr(tcp, 'dport'):
          if tcp.dport == 80 and len(tcp.data) > 0:
            http = dpkt.http.Request(tcp.data)
            ret = shannon.shannon(tcp.data)
            ret2 = chisqr.chisqr(tcp.data)

            # ascii test
            if (ret[1] < 128):
              asc.append(tcp.data)
              

            # shannon entropy test
            if (ret[0] < 6):
              sha.append(tcp.data)
              # print counter, ret[0]

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
              # print counter, ret[0]
              
            # chi squared test
            if (ret2 > 1500):
              chi.append(tcp.data)         
              # print counter, ret2

      if ip.p==dpkt.ip.IP_PROTO_TCP: 
         tcpcounter+=1

      if ip.p==dpkt.ip.IP_PROTO_UDP:
         udpcounter+=1


  # print "Total number of packets in the pcap file: ", counter
  # print "Total number of ip packets: ", ipcounter
  # print "Total number of tcp packets: ", tcpcounter
  # print "Total number of udp packets: ", udpcounter

  words1, packets1 = dictSearch.dictSearch(asc)
  words2, packets2 = dictSearch.dictSearch(chi)
  words3, packets3 = dictSearch.dictSearch(sha)


  payloads=[]
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
  for word, line in zip(words3, packets3):
    line = format(line)
    payloads.append(line)
    # print word
    # print line
    # print


  data = {}
  data['payloads'] = payloads
  json_data = json.dumps(data)

  f.close()


filenames = glob.glob('*.pcap')
for filename in filenames:
  # print "***************************** " + filename + " *******************************"
  analyze(filename)




