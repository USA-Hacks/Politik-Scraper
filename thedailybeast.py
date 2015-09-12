#!/usr/bin/python

from newspaper import Article
from bs4 import BeautifulSoup
import requests
import logging

from outputwriter import OutputWriter, political_keywords

url_template = u'http://www.thedailybeast.com/topics/politics.%s.html'
website_name = '/articles'
host_url = 'http://www.thedailybeast.com'
num_pages = 100

article_urls = []
entity_id = 1476

def get_website_url(page_num):
	return url_template % (str(page_num))


for page in range(num_pages + 1):
        print 'Page: ' + str(page)
	url = get_website_url(page)
        article = requests.get(url)

	soup = BeautifulSoup(article.text, 'html.parser')
	for link in soup.find_all('a'):
		href = link.get('href')
		if href != None:
			if website_name in href:
				article_urls.append(host_url + href)

article_urls = list(set(article_urls))
print article_urls
out = OutputWriter()
for article_url in article_urls:
	try:
		article = Article(article_url)
		article.download()
		article.parse()
		article.nlp()
		score = len([i for i in political_keywords if i in article.keywords])
		if score > 0:
			out.output('Democrat', article.text, entity_id, score)
			entity_id += 1
	except:
		print 'Error: ' + article_url
out.close()
