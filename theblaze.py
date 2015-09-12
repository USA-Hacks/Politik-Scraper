#!/usr/bin/python

from newspaper import Article
from bs4 import BeautifulSoup
import requests
import logging

from outputwriter import OutputWriter, political_keywords

url_template = u'http://www.theblaze.com/stories/category/politics/page/%s/'
website_name = 'http://www.theblaze.com/stories'
num_pages = 100

article_urls = []
entity_id = 540

def get_website_url(page_num):
	return url_template % (str(page_num))


for page in range(1, num_pages + 1):
        url = get_website_url(page)
        article = requests.get(url)

	soup = BeautifulSoup(article.text, 'html.parser')
	
	for link in soup.find_all('a'):
		href = link.get('href')
		if website_name in href and 'category' not in href:
			article_urls.append(href)

article_urls = list(set(article_urls))

out = OutputWriter()
for article_url in article_urls:
	try:
		article = Article(article_url)
		article.download()
		article.parse()
		article.nlp()
		score = len([i for i in political_keywords if i in article.keywords])
		if score > 0:
			out.output('Republican', article.text, entity_id, score)
			entity_id += 1
	except:
		print 'Error: ' + article_url
out.close()
