import os
import time
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import bs4 as bs
import urllib.request

path = "C:/Users/dasei/Desktop/intraQuarter"

class Client(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
    
    def on_page_load(self):
        self.app.quit()


def Check_Yahoo():
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    for stock in stock_list[1:]:
        try:
            stock = stock.replace('C:/Users/dasei/Desktop/intraQuarter/_KeyStats\\', '').upper()
            print(stock)
            url = 'https://finance.yahoo.com/quote/' + stock + '/key-statistics?p=' + stock
            client_response = Client(url)
            source = client_response.mainFrame().toHtml()
            #soup = bs.BeautifulSoup(source, 'lxml')

            save = path + '/_KeyStats/forward/' + str(stock) + '.html'
            store = open(save, 'w')
            store.write(str(source))
            store.close()

        except Exception as e:
            print('Exception:', str(e))
            time.sleep(1)

Check_Yahoo()