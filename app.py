from flask import Flask
from bs4 import BeautifulSoup
import urllib

app = Flask(__name__)

def getImages():
	adPage = BeautifulSoup(urllib.urlopen('http://reddit.com/r/ads').read())
	for div in adPage.find_all('div'):
		if div.get('id') == 'siteTable':
			print div.prettify()

getImages()

if __name__ == '__main__':
	app.run()