from flask import Flask
from bs4 import BeautifulSoup
import urllib
import redis
import threading
import urlparse
import os

app = Flask(__name__)

REDDIT_BASE_URL = 'http://reddit.com/r/ads'

# Configuring redis
# redisURL = urlparse.urlparse(os.environ.get('redis://rediscloud:xe4SRK3ne879ejFk@pub-redis-14323.us-east-1-3.1.ec2.garantiadata.com:14323'))
r = redis.StrictRedis(host='pub-redis-14323.us-east-1-3.1.ec2.garantiadata.com', port=14323, db=0)

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
			maxCount = 20
			for childDiv in div:
				if counter == maxCount:
					break
				if 'thing' in childDiv.get('class'):
					voteDelta = getVoteDelta(childDiv.attrs)
					sourceLink = getSourceLink(childDiv)
					output[sourceLink] = voteDelta
				counter += 1

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec) 
		func()  
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t

def runCycle():
	newStore = getImages()
	for image in newStore:
		currentCount = -9999
		try:
			currentCount = r.get(image)
		except:
			pass
		if newStore[image] > currentCount:
			r.set(image, currentCount)

set_interval(runCycle, 10)

if __name__ == '__main__':
	app.run()