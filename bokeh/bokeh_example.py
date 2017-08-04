import numpy as np
import urllib2
import matplotlib.dates as mdates

from bokeh.plotting import figure, show, output_file, vplot
#from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

#download stock data
stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/AAPL/chartdata;type=quote;range=1y/csv'
source_code = urllib2.urlopen(stock_price_url).read()
stock_data = []
split_source = source_code.split('\n')

for line in split_source:
    split_line = line.split(',')
    if len(split_line) == 6:
        if 'values' not in line and 'labels' not in line:
            stock_data.append(line)

date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters={0: mdates.strpdate2num('%Y%m%d')})

def datetime(x):
    return np.array(x, dtype=np.datetime64)

p1 = figure(x_axis_type = "datetime")
p1.title = "Stock Closing Prices"
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

p1.line(date, closep, color='#A6CEE3', legend='AAPL')

aapl = np.array(closep)
aapl_dates = np.array(date, dtype=np.datetime64)

window_size = 30
window = np.ones(window_size)/float(window_size)
aapl_avg = np.convolve(aapl, window, 'same')

p2 = figure(x_axis_type="datetime")
p2.title = "AAPL One-Month Average"
p2.grid.grid_line_alpha = 0
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Price'
p2.ygrid.band_fill_color = "olive"
p2.ygrid.band_fill_alpha = 0.1

p2.circle(aapl_dates, aapl, size=4, legend='close',
          color='darkgrey', alpha=0.2)

p2.line(aapl_dates, aapl_avg, legend='avg', color='navy')

output_file("stocks.html", title="stocks.py example")

show(vplot(p1,p2))  # open a browser