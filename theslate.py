#!/usr/bin/python

from newspaper import Article
from bs4 import BeautifulSoup
import requests
import logging

from outputwriter import OutputWriter

url_template = u'http://www.slate.com/full_slate%s.html'
website_name = 'http://www.slate.com/'
num_pages = 100

article_urls = []

political_keywords = ['iran', 'obama', 'compaign', 'resolution', 'trump', 'republicans', 'democrats', 'bernie', 'election', 'voting', 'polls', 'hillary', 'bush', 'war', 'economy', 'abortion', 'gun', 'rights', 'conservative', 'liberal', 'liberty', 'privacy']

entity_id = 0

def get_website_url(page_num):
        if page_num == 0:
                return url_template % ('')
        else:
                return url_template % ('.' + str(page_num))


for page in range(num_pages + 1):
        url = get_website_url(page)
        article = requests.get(url)

	soup = BeautifulSoup(article.text, 'html.parser')
	
	for link in soup.find_all('a'):
		href = link.get('href')
		if website_name in href and 'full_slate' not in href:
			article_urls.append(href)

out = OutputWriter()
for article_url in article_urls:
	article = Article(article_url)
	article.download()
	article.parse()
	article.nlp()
	if len([i for i in political_keywords if i in article.keywords]) > 0:
		out.output('Democrat', article.text, entity_id, 3)
		entity_id += 1

out.close()
