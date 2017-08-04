from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('stop', 2),
        ('target', 2),
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataopen = self.datas[0].open

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Indicators for the plotting show
        #bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        #bt.indicators.ATR(self.datas[0], plot=False)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size

                # Profit taking sell limit order
                price = order.executed.price + self.params.target
                self.sell(exectype=bt.Order.Limit,
             			  price=price)
                self.log('SELL LIMIT CREATED, %.2f' % price)

                # Protective sell stop order
                price = order.executed.price - self.params.stop
                self.sell(exectype=bt.Order.Stop, 
						  price=price)
                self.log('SELL STOP CREATED, %.2f' % price)

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

                self.broker.cancel(order)
                
                self.log('self.order: '+str(order))

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:

				if self.dataclose[-1] < self.dataclose[-2]:            	

					# Buy market order
					price = self.dataclose[0]
					self.order = self.buy()
					self.log('BUY MARKET CREATED, %.2f' % price)

'''
        else:

        	# Sell if stop hit
        	if self.datalow[0] <= (self.price_executed - self.params.stop):
        		self.log('SELL CREATE, %.2f' % (self.price_executed - self.params.stop))

        	# Sell if profit target hit. If stop & target hit on same bar, consider it stopped out
        	elif self.datahigh[0] > (self.price_executed + self.params.target):
        		self.log('SELL MARKET CREATED, %.2f' % (self.price_executed + self.params.target))

        	# Don't exit position yet
        	else:
        		return

        	# Keep track of the created order to avoid a 2nd order
        	self.order = self.sell()
'''

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Create a Data Feed
    user = 'Scipio'
    datafile = 'ES_U16_5min.txt'
    datapath = '/Users/'+user+'/OneDrive/Documents/Programs/Python/backtrader/data/'+datafile
    data = bt.feeds.GenericCSVData(
        dataname=datapath,

	    fromdate=datetime.datetime(2016, 8, 1),
	    todate=datetime.datetime(2016, 8, 2),

	    dtformat=('%Y/%m/%d'),
	    tmformat=(' %H:%M:%S'),

	    datetime=0,
	    time=1,
	    open=2,
	    high=3,
	    low=4,
	    close=5,
	    volume=6,
	    openinterest=-1
        )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    #cerebro.broker.setcommission(commission=1.78, margin=500, mult=50)
    cerebro.broker.setcommission(commission=0.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot(style='bar')