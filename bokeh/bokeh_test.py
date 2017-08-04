import pandas as pd
from bokeh.plotting import figure, show, output_file
#from bokeh.models import Ticker

#load data into pandas dataframe
df = pd.read_csv('ES500Tick.txt')

#strip whitespace from headers
df.rename(columns=lambda x: x.strip(), inplace=True)

#combine Date and Time, convert to datetime
df['Datetime'] = df['Date'].map(str) + df['Time'].map(str)
df['Datetime'] = pd.to_datetime(df['Datetime'])

#calculate values for candles
mids = (df.Open + df.Last)/2
spans = abs(df.Last-df.Open)
inc = df.Last > df.Open
dec = df.Open > df.Last
w = 1000*10 #10 secs

#make figure
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, toolbar_location="left")

#make fixed ticks
p.xaxis[0].ticker.desired_num_ticks = len(df['Datetime'])

p.title = "ES Candlestick"
p.xaxis.major_label_orientation = .8
p.grid.grid_line_alpha=0.3

#plot high-low lines
p.segment(df.Datetime, df.High, df.Datetime, df.Low, color="black")

#plot up bars
p.rect(df.Datetime[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")

#plot down bars
p.rect(df.Datetime[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

output_file("candlestick.html", title="candlestick.py example")

show(p)  # open a browser