filepath = 'C:/Users/scipio/Desktop/F.US.EPM17.txt'
symbol = 'ES_M17'
dates = ['2017/6/6',
		 '2017/6/7',
		 '2017/6/8',
		 '2017/6/9',]

for date in dates:
	newfile = symbol+'_'+date.replace('/', '.')+'.txt'
	with open(filepath, 'rb') as sourcefile, open(newfile, 'w') as outfile:
	    for line in sourcefile:
	        if line.startswith(date) or line.startswith('Date'):
	            outfile.write(line)