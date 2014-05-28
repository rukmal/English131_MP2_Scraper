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
redisURL = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=redisURL.hostname, port=redisURL.port, password=redisURL.password)

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
					print 'Source link: ' + sourceLink + ' with a vote delta of ' + str(voteDelta)
				counter += 1

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec) 
		func()  
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t



if __name__ == '__main__':
	app.run()