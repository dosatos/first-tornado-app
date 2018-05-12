from tornado import web, gen
from tornado.escape import json_encode
from requests.exceptions import InvalidURL, ConnectionError
from sqlalchemy import desc

# own helping libs
import myparser
from models import Word, add_word, Sentiment, add_sentiment
from hashutils import RSAEncryption


class MainHandler(web.RequestHandler):
	""" Main page handler - manages the word cloud generation mechanics """
	def initialize(self, db_session):
		self.db_session = db_session()

	def get(self):
		self.render("index.html", 
				message="Enter a url above")

	def post(self):
		url = self.get_argument('url')
		try:
			data = myparser.get_words(url)
			if data:
				# if sucessfully exctracted data, add to db
				session = self.db_session
				# insert/update words to db
				for pair in data:
					add_word(pair, session)
				print(f"{len(data)} WORDS ADDED.")
				# print(data)
				# add sentiment
				sent = (url, 1)
				add_sentiment(sent, session)
				
				self.render("index.html", 
							message=f"Enjoy WordCloud of {url}",
							data=json_encode(data))
			else:
				self.render("index.html", message=f"No words were parsed from the website {url}.")
		except (ConnectionError, InvalidURL) as e:
			self.render("index.html", message=f"No words were parsed from the website {url}.")

class AdminHandler(web.RequestHandler):

	def initialize(self, db_session):
		self.db_session = db_session()

	def get(self):
		rsa = RSAEncryption()
		session = self.db_session
		data = session.query(Word).order_by(desc(Word.frequency)).all()
		data = [ (rsa.decrypt(row.encrypted_word), row.frequency) for row in data ]
		# print(data[:10], data[-10:])
		self.render("admin.html", data=json_encode(data))