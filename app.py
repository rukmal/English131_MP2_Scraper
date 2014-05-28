from flask import Flask
from bs4 import BeautifulSoup
import urllib

app = Flask(__name__)

def getImages():
	adPage = BeautifulSoup(urllib.urlopen('http://reddit.com/r/ads').read())
	for div in adPage.find_all('div'):
		if div.get('id') == 'siteTable':
			counter = 0
			maxCount = 10
			for childDiv in div:
				if counter == maxCount:
					break
				if 'thing' in childDiv.get('class'):
					voteDelta = # function taking params
					sourceLink = # function taking params
					redditLink = # function taking params
				counter += 1
			print counter

getImages()

if __name__ == '__main__':
	app.run()