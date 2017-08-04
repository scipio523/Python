from selenium import webdriver
import yaml
from bs4 import BeautifulSoup
import mechanize
import time

url = "http://www.bing.com/"

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)')]

br.open(url)

for query in range(0,5):
	query = str(query)
	print query
	br.select_form(nr=0)
	br.form["q"] = query
	br.submit()
	if br.title() != query + " - Bing":
		print "Query failed!"	
	else:
		print "Succesfully searched Bing!\nQuery: "+query
	time.sleep(1)



