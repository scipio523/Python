import urllib
import re
from bs4 import BeautifulSoup
import urlparse
import mechanize
import time

url= "https://www.facebook.com/login"

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)')]

br.open(url)

for i in br.forms():
	print i

email = raw_input("Username & Email : ")
password = raw_input("Password: ")

br.select_form(nr=0)

br.form["email"] = email
br.form["pass"] = password
br.submit()

if br.title() != "Facebook":
	print "Name or pass Wrong !"
	time.sleep(3)
else:
	print "Facebook Login Success ! \n \tUsername : "+email+"\n"+"\tPassword : "+password+"\n"
	time.sleep(5)

