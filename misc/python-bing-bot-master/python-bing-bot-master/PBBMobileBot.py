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
import PythonMobileBingBot

class MobileBot(object):
    
    def __init__(self,withBrowser,withConfig):
        self.browser = withBrowser
        self.config = withConfig
        self.facebookAccounts = self.config['FACEBOOK_EMAIL']
        self.outlookAccounts = self.config['OUTLOOK_EMAIL']
        self.facebookPasswords = self.config['FACEBOOK_PASSWORD']
        self.outlookPasswords = self.config['OUTLOOK_PASSWORD']    
        self.desktopSearchNumber = self.config['NUMBER_OF_DESKTOP_SEARCHES'][0]
        self.mobileSearchNumber = self.config['NUMBER_OF_MOBILE_SEARCHES'][0]
        self.facebookCredits = []
        self.outlookCredits = []
        self.detector = PBBDetector.Detector(withBrowser)
        self.searcher = PBBSearch.Search(withBrowser)
        self.generator = PBBSearchQueries.QueryGenerator()
        self.login = PBBLogin.Login(withBrowser)

    def quit_browser(self):
        print "Quitting mobile browser"
        self.browser.quit()

    def load_yaml_file(fileName):
        fileData = open(fileName)
        yamlFile = yaml.load(fileData)
        return yamlFile

    def begin_searching(self):
        if len(self.outlookAccounts) > 0:
            self.begin_outlook_searches()
        if len(self.facebookAccounts) > 0:
            self.begin_facebook_searches()

        for q in range(0,len(self.outlookAccounts)):
            account = self.outlookAccounts[q]
            credit = self.outlookCredits[q]
            print 'Credits for ' + account + ': ' + credit

        for p in range(0,len(self.facebookAccounts)):
            account = self.facebookAccounts[p]
            credit = self.facebookCredits[p]
            print 'Credits for ' + account + ': ' + credit

        self.quit_browser()

    def begin_outlook_searches(self):
        for y in range(0,len(self.outlookAccounts)):
            account = (self.outlookAccounts[y],self.outlookPasswords[y])
            self.login.login_to_outlook(account)
            self.detector.navigate_to_rewards_pane()
            self.detector.detect_desktop_searches()
            self.detector.detect_mobile_searches()
            self.detector.detect_offer_for_mobile()
            self.detector.detect_and_claim_free_offer()
            outlookUsername = self.outlookAccounts[y]
            desktopSearches = self.detector.mobileMultiplier * self.detector.mobileDifference
            for i in range(0,desktopSearches):
                print 'Searching ' + outlookUsername + ' # ' + repr(i + 1) + ' of ' + repr(desktopSearches)
                searchString = self.generator.generate_search_string()
                self.searcher.search_bing_with_query(searchString)
            self.detector.navigate_to_rewards_pane()
            self.detector.detect_desktop_searches()
            self.detector.detect_mobile_searches()
            self.detector.detect_and_claim_free_offer()
            print self.detector.description()
            self.browser.get("http://www.bing.com")
            credits = self.detector.detect_total_mobile_credits()
            self.outlookCredits.append(credits)
            self.login.logout_from_mobile_bing()
            
        print "Finished with Outlook Searches"

    def begin_facebook_searches(self):
        for x in range(0, len(self.facebookAccounts)):
            account = (self.facebookAccounts[x],self.facebookPasswords[x])
            self.login.login_to_facebook(account)
            self.detector.navigate_to_rewards_pane()
            self.detector.detect_desktop_searches()
            self.detector.detect_mobile_searches()
            self.detector.detect_offer_for_mobile()
            self.detector.detect_and_claim_free_offer()
            facebookUserName = self.facebookAccounts[x]
            mobileSearches = self.detector.mobileMultiplier * self.detector.mobileDifference
            print "Need " + repr(mobileSearches) + " mobile searches"
            for i in range(0,mobileSearches):
                print 'Searching ' + facebookUserName + ' # ' + repr(i + 1) + ' of ' + repr(mobileSearches)
                searchString = self.generator.generate_search_string()
                self.searcher.search_bing_with_query(searchString)
            self.detector.navigate_to_rewards_pane()
            self.detector.detect_desktop_searches()
            self.detector.detect_mobile_searches()
            print self.detector.description()
            self.browser.get("http://www.bing.com")
            credits = self.detector.detect_total_mobile_credits()
            self.facebookCredits.append(credits)
            self.login.logout_from_mobile_bing()
        print "Finished With Facebook Searches"