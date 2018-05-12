import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import Counter
import re
import nltk
import operator


def tag_visible(element):
	""" returns if a tag is visible  """
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True


def parse_text_from(content):
	""" retrieves text from visible texts """
	soup = BeautifulSoup(content, 'html.parser')
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)  
	return u" ".join(t.strip() for t in visible_texts)


def custom_filter(text):
	""" filters for verbs and nouns using NLTK library and regex """
	regex = re.compile('[^a-zA-Z]{2,}')
	text = regex.sub(' ', text.lower())
	# text = re.sub('[^a-zA-Z]$', ' ', text.lower())
	tokens = nltk.word_tokenize(text)
	text = nltk.Text(tokens)
	tags = nltk.pos_tag(text)

	verbs_and_nouns = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 
		'NN', 'NNS', 'NNP', 'NNPS']
	counts = Counter(word for word, tag in tags 
		if tag in verbs_and_nouns and len(word) > 2)
	return counts.most_common(100)


def get_words(original_url):
	""" get word-frequency pair """
	url = original_url
	# regex = re.compile( r'^(?:http|ftp)s?://')
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if not re.match(regex, url):
		url = "http://" + url
	page = requests.get(url)
	words = custom_filter(parse_text_from(page.content))
	return words