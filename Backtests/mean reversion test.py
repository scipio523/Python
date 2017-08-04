import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl
import time
quandl.ApiConfig.api_key = "24j97rXQ8QwNoN1ssXbj"

#---------------------------------------------------#
# Test
def getdata(ticker, start=None, end=None):
	ohlc = quandl.get(ticker,
				  start_date=start,
				  end_date=end
				  ) 
	return ohlc


def sharpe(rets):
	mean = rets.mean()

	if rets.std() == 0: 
		std = 0.0000001
	else:
		std = rets.std()

	return (mean / std) * (252 ** .5)


# If both close-close return and close-open returns below respective thresholds, buy and hold until close.
def backtest(ohlc, ccThresh=-0.25, coThresh=-0.1):
	stratData = pd.DataFrame(index=ohlc.index)
	stratData['cc'] = 100*ohlc['Close'].pct_change()
	stratData['co'] = 100*(ohlc['Open']/ohlc['Close'].shift()-1)
	stratData['oc'] = 100*(ohlc['Close']/ohlc['Open']-1)

	idx = (stratData['cc'] < ccThresh).shift() & (stratData['co'] < coThresh)
	idx[0] = False

	stratData['goLong'] = idx
	stratData['pnl'] = 0.
	stratData['pnl'][idx] = stratData['oc'][idx]

	return stratData


if __name__ == '__main__':

	# download data from quandl
	ohlc = getdata('YAHOO/XLP')
	del(ohlc['Volume'], ohlc['Adjusted Close'])

	#ohlc = getdata('CHRIS/CME_ES1', start='2002-01-01', end='2004-01-01')
	#ohlc.rename(columns={'Last': 'Close'}, inplace=True)
	#del(ohlc['Change'], ohlc['Settle'], ohlc['Volume'], ohlc['Open Interest'])

	# run backtest with baseline parameters and plot pnl
	stratData = backtest(ohlc)
	print 'baseline sharpe: %.2f' % sharpe(stratData['pnl'])
	plt.subplot(2,2,1)
	stratData['pnl'].cumsum().plot(title='baseline', grid=True)

	# optimize for highest sharpe; make heatmap
	ccThresh = np.linspace(-3, 3, 30)
	coThresh = np.linspace(-3, 3, 30)
	SH = np.zeros((len(ccThresh), len(coThresh)))

	for i, cc in enumerate(ccThresh):
		for j, co in enumerate(coThresh):
			stratData = backtest(ohlc, ccThresh=cc, coThresh=co)
			SH[i,j] = sharpe(stratData['pnl'])

	plt.subplot(2,2,2)
	plt.pcolormesh(coThresh, ccThresh, SH)
	plt.xlabel('Opening gap [%]')
	plt.ylabel('previous day change [%]')
	plt.colorbar()

	i,j = np.unravel_index(SH.argmax(), SH.shape)

	# run backtest with optimum parameters and plot pnl
	stratData = backtest(ohlc, ccThresh[i], coThresh[j])
	print 'optimum CC: %.2f' % ccThresh[i]
	print 'optimum CO: %.2f' % coThresh[j]
	print 'optimum sharpe: %.2f' % sharpe(stratData['pnl'])
	plt.subplot(2,2,3)	
	stratData['pnl'].cumsum().plot(grid=True, title='optimal')

	# show plots
	plt.subplots_adjust(hspace = 0.8)
	plt.show()