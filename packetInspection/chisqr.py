#==============================================================================
# SPRING 2016 JUNIOR INDEPENDENT WORK
#title           : chisqr.py
#description     : This program calculates the chi squared value of the payload
#                : of a packet of transmitted data and returns the result
#author          : Daniel Wood
#advisor         : Nick Feamster
#date            : May 5, 2017
#usage           : chisqr.chisqr("testpayload")
#==============================================================================

import math
import sys
import random


def chisqr(data):
	N = 256
	freq = [0] * N
	size = len(data)
	for c in data:
		freq[ord(c)] += 1
	chi = 0.
	for f in freq:
		chi += (f - size/float(N)) * (f - size/float(N)) / (size/float(N))
	return chi
