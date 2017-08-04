#returns CSV file with Yahoo data for chosen ticker
import urllib

base_url = "http://ichart.finance.yahoo.com/table.csv?s="

def make_url(ticker_symbol):
    return base_url + ticker_symbol

output_path = '/Users/Scipio/OneDrive/Documents/Programs/Python'

def make_filename(ticker_symbol, directory=""):
    return output_path + "/" + directory + "/" + ticker_symbol + ".csv"

def get_data(ticker_symbol, directory=""):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol, directory))
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), 'w')
        outfile.write(e.content)
        outfile.close()
        