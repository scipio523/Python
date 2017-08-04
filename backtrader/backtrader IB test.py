import backtrader as bt

#create a strategy
class Strat(bt.Strategy):
	def __init__(self):
		self.dataclose = self.datas[0].close

	def log(self, txt, dt=None):
		dt = dt or self.datas[0].datetime.datetime(0)
		print('%s, %s' % (dt.isoformat(), txt))

	def next(self):
		self.log('Close, %.2f' % self.dataclose[0])

#create a cerebro entity
cerebro = bt.Cerebro()

#add a strategy
cerebro.addstrategy(Strat)

#get datafeed
ibstore = bt.stores.IBStore(host='127.0.0.1', port=7497, clientId=999)
data = ibstore.getdata(dataname='AAPL-STK-SMART-USD',
					   timeframe=bt.TimeFrame.Ticks,
                       compression=1,  # 1 is the default
                       )

#add datafeed to cerebro
cerebro.adddata(data)

#set broker as IB
cerebro.broker = ibstore.getbroker()

#run over everything
cerebro.run()

#print cerebro.broker.getcash()