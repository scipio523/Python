from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Search(object):
	def __init__(self,withBrowser):
		self.browser = withBrowser

	def search_bing_with_query(self,searchText):
	    self.browser.get("http://www.bing.com")
	    time.sleep(5)
	    searchField = self.browser.find_element_by_name('q')
	    searchField.send_keys(searchText + Keys.RETURN)
	    time.sleep(10)