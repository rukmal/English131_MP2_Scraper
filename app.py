from flask import Flask
from bs4 import BeautifulSoup
import urllib
import redis

app = Flask(__name__)

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

getImages()

if __name__ == '__main__':
	app.run()