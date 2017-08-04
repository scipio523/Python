from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message  

new_symbolinput = ['AAPL', 'ACE']
newDataList = []  
dataDownload = []  

def historical_data_handler(msg):  
    global newDataList  
    print (msg.reqId, msg.date, msg.close)
    if ('finished' in str(msg.date)) == False:  
        new_symbol = new_symbolinput[msg.reqId]  
        dataStr = '%s, %s, %s' % (new_symbol, strftime("%Y-%m-%d", localtime(int(msg.date))), msg.close)  
        newDataList = newDataList + [dataStr]
    else:  
        new_symbol = new_symbolinput[msg.reqId]  
        filename = 'minutetrades' + new_symbol + '.csv'  
        csvfile = open('csv_day_test/' + filename,'w')  
        for item in newDataList:  
            csvfile.write('{} \n'.format(item))
        csvfile.close()  
        newDataList = []  
        global dataDownload  
        dataDownload.append(new_symbol)  

def reply_handler(msg):
    print "Server Response: %s, %s" % (msg.typeName, msg)

con = ibConnection(port=7497,clientId=999)  
con.register(historical_data_handler, message.historicalData)  
con.registerAll(reply_handler)
con.connect()  

symbol_id = 0  
for i in new_symbolinput:  
    print (i)  
    qqq = Contract()  
    qqq.m_symbol = i  
    qqq.m_secType = 'STK'  
    qqq.m_exchange = 'SMART'  
    qqq.m_currency = 'USD'
    #qqq.m_expiry = '201609'
    con.reqHistoricalData(symbol_id, qqq, '', '1 D', '5 mins', 'TRADES', 1, 1)  

    symbol_id = symbol_id + 1  
    sleep(3)

print dataDownload

'''
filename = 'downloaded_symbols.csv'  
csvfile = open(filename,'w')  
for item in dataDownload:  
    csvfile.write('%s \n' % item)  
csvfile.close()
'''