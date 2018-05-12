import os
# from app import settings
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from hashutils import RSAEncryption, salt_string
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


class Word(Base):
	__tablename__ = 'words'

	salted_word = Column('salted_word', String, primary_key=True) # salted word
	encrypted_word = Column('word', String, unique=True)  # asymetrically encrypted word
	frequency = Column('frequency', Integer) # total frequency


def add_word(entry, session):
	word = Word()
	rsa = RSAEncryption()
	given_word, frequency = entry
	word.salted_word, word.encrypted_word, word.frequency = salt_string(given_word), rsa.encrypt(given_word), frequency
	try:
		row = session.query(Word).filter(Word.salted_word == word.salted_word).first()
		row.salted_word, row.encrypted_word = salt_string(given_word), rsa.encrypt(given_word)
		f = row.frequency + frequency
		row.frequency = f # increment words frequency with each new url fetching
		session.commit()
	except AttributeError as e:
		session.rollback()
		session.add(word)
		session.commit()


class Sentiment(Base):
	__tablename__ = 'sentiment'

	salted_url = Column('salted_url', String, primary_key=True)  # salted url
	url = Column('url', String, primary_key=True)  # url
	analysis = Column('analysis', Integer)  # sentiment: positive or negative


def add_sentiment(entry, session):
	sentiment = Sentiment()
	rsa = RSAEncryption()
	url, analysis = entry
	
	sentiment.salted_url = salt_string(url)
	sentiment.url = url
	sentiment.analysis = analysis

	print(sentiment.url, sentiment.salted_url, sentiment.analysis)
	try:
		row = session.query(Sentiment).filter(Sentiment.url == url).first()
		row.analysis = analysis # if the analysis has changed since the last url fetching
		session.commit()
		print("SENTIMENT UPDATED")
	except AttributeError as e:
		print("NEW URL IN DB", url)
		session.rollback()
		session.add(sentiment)
		session.commit()
		print("SENTIMENT ADDED")