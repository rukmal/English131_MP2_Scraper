from flask import Flask
from bs4 import BeautifulSoup
import urllib
import threading
import urlparse
import os
import json

REDDIT_BASE_URL = 'http://reddit.com/r/ads'

def getVoteDelta(divAttrsDict):
	upVotes = int(divAttrsDict['data-ups'])
	downVotes = int(divAttrsDict['data-downs'])
	return upVotes - downVotes

def getSourceLink(divAttrsDict):
	for link in divAttrsDict.find_all('a'):
		try: # this is because some of the links are blank
			if 'may-blank' in link.get('class'):
				return link.get('href')
		except:
			pass

def getImages():
	adPage = BeautifulSoup(urllib.urlopen(REDDIT_BASE_URL).read())
	output = dict()
	for div in adPage.find_all('div'):
		if div.get('id') == 'siteTable':
			counter = 0
			maxCount = 30
			for childDiv in div:
				if counter == maxCount:
					break
				if 'thing' in childDiv.get('class'):
					voteDelta = getVoteDelta(childDiv.attrs)
					sourceLink = getSourceLink(childDiv)
					output[sourceLink] = voteDelta
				counter += 1
	return output

oldStore = getImages()

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec) 
		func()  
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t

def runCycle():
	newStore = getImages()
	print 'Running job'
	for image in newStore:
		currentCount = -9999
		try:
			currentCount = oldStore[image]
		except:
			pass
		if newStore[image] > currentCount:
			oldStore[image] = newStore[image]
	outfile = open('out.json', 'w')
	outfile.write(json.dumps(oldStore))
	outfile.close()

set_interval(runCycle, 60)