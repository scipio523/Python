import urllib2
import time
import datetime as dt
import os.path

stocks = ['GDX', 'GLD']
period = '9y'

def get_data(stock):
    try:
        filepath = 'data/'+stock+'.txt'
        if os.path.exists(filepath): os.remove(filepath)
        print 'Currently Pulling',stock
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+period+'/csv'
        try:
            sourceCode = urllib2.urlopen(urlToVisit).read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine)==6:
                    if 'values' not in eachLine:
                        saveFile = open(filepath, 'a')
                        convdate = dt.datetime.fromtimestamp(float(splitLine[0]))
                        eachLine = str(convdate) + eachLine[eachLine.find(','):]
                        saveFile.write(eachLine+'\n')
        except Exception, e:
            print str(e), 'failed to organize pulled data.'
    except Exception,e:
        print str(e), 'failed to pull pricing data'

for stock in stocks:
    get_data(stock)
