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

# freq = [0] * 256
# for i in xrange(100000):
# 	freq[random.randint(0,100)] += 1
# chi = 0.
# size = 100000
# N = 256
# for f in freq:
# 	chi += (f - size/float(N)) * (f - size/float(N)) / (size/float(N))
# print chi