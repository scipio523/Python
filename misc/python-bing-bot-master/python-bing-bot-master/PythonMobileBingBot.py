from selenium import webdriver
import PBBSearchQueries
import os,sys
from selenium.webdriver.common.keys import Keys
import time
import yaml
from yaml import load, dump
import PBBDetector
import PBBSearch
import PBBLogin

def SetWorkingDirectory(self):
    os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def LoadYAMLFile(fileName):
    fileData = open(fileName)
    yamlFile = yaml.load(fileData)
    return yamlFile

def Search(browserObject,searchText):
    browserObject.get("http://www.bing.com")
    time.sleep(5)
    searchField = browserObject.find_element_by_name('q')
    searchField.send_keys(searchText + Keys.RETURN)
    time.sleep(10)

def StartMobileSearch(self):
    SetWorkingDirectory()
    config = LoadYAMLFile('config.yaml')
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
    mobileBrowser = webdriver.Chrome(chrome_options=options)
    facebookAccounts = config['FACEBOOK_EMAIL']
    outlookAccounts = config['OUTLOOK_EMAIL']
    facebookPasswords = config['FACEBOOK_PASSWORD']
    outlookPasswords = config['OUTLOOK_PASSWORD']

    desktopSearchNumber = config['NUMBER_OF_DESKTOP_SEARCHES'][0]
    mobileSearchNumber = config['NUMBER_OF_MOBILE_SEARCHES'][0]

    for y in range(0,len(outlookAccounts)):
        account = (outlookAccounts[y],outlookPasswords[y])
        PBBLogin.LogInToOutlook(mobileBrowser,account)
        outlookUserName = outlookAccounts[y]
        PBBDetector.NavigateToRewardsPane(mobileBrowser)
        PBBDetector.DetectAndClaimFreeOffer(mobileBrowser)
        for j in range(0,mobileSearchNumber):
            print 'Searching ' + outlookUserName + ' # ' + repr(j + 1)
            searchString = PBBSearchQueries.GetSearchString()
            PBBSearch.Search(mobileBrowser,searchString)
        PBBLogin.LogOutOfMobileBing(mobileBrowser)

    for x in range(0, len(facebookAccounts)):
        account = (facebookAccounts[x],facebookPasswords[x])
        PBBLogin.LogInToFacebook(mobileBrowser,account)
        facebookUserName = facebookAccounts[x]
        PBBDetector.NavigateToRewardsPane(mobileBrowser)
        PBBDetector.DetectAndClaimFreeOffer(mobileBrowser)
        for i in range(0,mobileSearchNumber):
            print 'Searching ' + facebookUserName + ' # ' + repr(i + 1)
            searchString = PBBSearchQueries.GetSearchString()
            PBBSearch.Search(mobileBrowser,searchString)
        PBBLogin.LogOutOfMobileBing(mobileBrowser)

    mobileBrowser.quit()
    print "Finished with Mobile Searches"


