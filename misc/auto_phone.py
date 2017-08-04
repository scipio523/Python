import urllib
import mechanize
from bs4 import BeautifulSoup
import re

def getGoogleMapsLinks(searchTerm):
	searchTerm=searchTerm.replace(" ","+")
	url="https://www.google.com/maps/search/searchTerm/@42.979339,-89.382005,10z/data=!3m1!4b1"
	resultsArr=[]
	br=mechanize.Browser()
	br.set_handle_robots(False)
	br.addHeaders=[('User-Agent','Google Chrome')]

	htmltext=br.open(url,timeout=3.0).read()
	soup=BeautifulSoup(htmltext)
	searchres=soup.findAll('div')
	print searchres

getGoogleMapsLinks("Driveway paving")
