from selenium import webdriver
import PBBSearchQueries
import PBBDesktopBot
import PBBMobileBot
import os,sys
from selenium.webdriver.common.keys import Keys
import time
import yaml
from yaml import load, dump

def set_working_directory():
    os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def load_yaml_file(fileName):
	fileData = open(fileName)
	yamlFile = yaml.load(fileData)
	return yamlFile

def main(argv=None):
    if argv is None:
    	argv = sys.argv
	set_working_directory()
	config = load_yaml_file('config.yaml')
	path = config['CHROMEDRIVER_PATH'][0]
	print "Initializing desktop browser at path " + path
	desktopBrowser = webdriver.Chrome(path)
	desktopBrowser.set_window_size(1280,1024)
	config = load_yaml_file('config.yaml')
	desktopBot = PBBDesktopBot.DesktopBot(desktopBrowser,config)
	desktopBot.begin_searching()
	options = webdriver.ChromeOptions()
	options.add_argument('--user-agent=Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
	mobileBrowser = webdriver.Chrome(path,chrome_options=options)
	print "Initializing mobile browser"
	mobileBot = PBBMobileBot.MobileBot(mobileBrowser,config)
	mobileBot.begin_searching()
	print "All finished up..."
	return 1

main()
time.sleep(3)