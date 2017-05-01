import sys

def dictSearch(info):
	# filename="medicalDict.txt"
	# filename = "1000names.txt"
	filename = "105medicalTerms.txt"
	with open(filename) as f:
		lines = f.readlines()

	lines = [line.rstrip('\n') for line in open(filename)]

	packets=[]
	words=[]

	for string in info:
		for word in lines:
			if word in string:
				if string not in packets:
					packets.append(string)
				if word not in words:
					words.append(word)

	return words, packets