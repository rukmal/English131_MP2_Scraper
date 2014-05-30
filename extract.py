import json

infile = 'out.json'
outfile = 'final.csv'

parsed = dict()

for line in open(infile, 'r').readlines():
	parsed = json.loads(line)

newOrder = dict()

for item in parsed:
	if parsed[item] not in newOrder:
		newOrder[parsed[item]] = list()
	newOrder[parsed[item]].append(item)

keys = newOrder.keys()

keys.sort()
keys.reverse()

counter = 0
outBuffer = ''

for key in keys:
	for url in newOrder[key]:
		if counter == 10:
			break
		counter += 1
		outBuffer += str(key) + ',' + url + "\n"

outputFile = open(outfile, 'w')
outputFile.write(outBuffer)
outputFile.close()