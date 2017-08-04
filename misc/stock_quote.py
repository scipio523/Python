import urllib
import re

url="http://www.google.com/finance?q=GDX"
htmlfile=urllib.urlopen(url)
htmltext=htmlfile.read()
regex='<span id="ref_[^.]*_l">(.+?)</span>'
pattern=re.compile(regex)
price=re.findall(pattern,htmltext)
print price

