# English 131 Major Paper 2 Reddit Scraper

Reddit scraper that scrapes the subbreddit ```/r/ads``` for the top 10 most popular image ads, saves them along with the number of votes, which it the concatenates to give me a list of the 10 most popular Reddit advertisements for a given period of time.

**NOTE: This program saves the highest vote of a post, over a period of time.**

## Usage

- Clone the repository by running the following:
```bash
$ git clone https://github.com/rukmal/English131_MP2_Scraper.git
```

- Install all requirements using pip using the following:
```bash
$ pip install -r requirements.txt
```

- Run the application locally, or deploy to Heroku for continuous scraping.

	- Running the application locally:
	```bash
	$ python app.py
	```
	
	- Deploying to Heroku:
	```bash
	$ heroku create <app_name_here>
	$ git push heroku master
	```

## Tech Stack

- Python redis library ```redis``` for storage

- Beautiful soup for parsing web page, from python package ```bs4```

- ```urllib``` for loading web pages

## Contact

This is an open source project released under the [MIT License](LICENSE). Contact me if you want to suggest an improvement, or fork and send a pull request!

Follow me on Twitter ([@rukmal_w](http://twitter.com/rukmal_w)) and [GitHub](http://github.com/rukmal).

http://rukmal.me