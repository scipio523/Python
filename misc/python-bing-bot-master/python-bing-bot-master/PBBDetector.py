import time
from selenium import webdriver

class Detector(object):

    def __init__(self,withBrowser):
        self.browser = withBrowser
        self.mobileSearchMin = 0
        self.mobileSearchMax = 0
        self.desktopSearchMin = 0
        self.desktopSearchMax = 0
        self.mobileDifference = 0
        self.desktopDifference = 0
        self.mobileMultiplier = 0
        self.desktopMultiplier = 0

    def detect_total_credits(self):
        elements = self.browser.find_elements_by_xpath('//*[@id="id_rc"]')
        for element in elements:
            print "Total Credits for this account: " + element.text
            return element.text

    def detect_total_mobile_credits(self):
        self.browser.get('http://www.bing.com/rewards/dashboard')
        time.sleep(5)
        elements = self.browser.find_elements_by_xpath('//*[@id="id_rc"]')
        for element in elements:
            print "Total Credits for this account: " + element.text
            return element.text

    def navigate_to_rewards_pane(self):
        print "Navigating to Rewards pane"
        self.browser.get('http://www.bing.com')
        time.sleep(4)
        self.browser.get('http://www.bing.com/rewardsapp/bepflyoutpage')
        time.sleep(3)

    def detect_mobile_searches(self):
        #Finds the progress/total of mobile searches
        elements = self.browser.find_elements_by_class_name('offertitle')
        for element in elements:
            if element.text.find('Mobile search-') > -1:
                stringLength = len(element.text)
                index = element.text.find(' of ')
                startPoint = index + 4
                creditsIndex = element.text.find(' credits')
                progressNumber = element.text[element.text.find('-') + 1:element.text.find(' of ')]
                totalNumber = element.text[startPoint:creditsIndex]
                self.mobileSearchMin = int(progressNumber)
                self.mobileSearchMax = int(totalNumber)
        if self.mobileSearchMin < self.mobileSearchMax:
            self.mobileDifference = self.mobileSearchMax - self.mobileSearchMin
            print "You need " + repr(self.mobileDifference) + " more mobile points"
        elif self.mobileSearchMin == self.mobileSearchMax:
            self.mobileDifference = 0
            print "You have all mobile searches today."


    def detect_desktop_searches(self):
        #Finds the progress/total of desktop searches
        elements = self.browser.find_elements_by_class_name('offertitle')
        for element in elements:
            if element.text.find('PC search-') > -1:
                stringLength = len(element.text)
                index = element.text.find(' of ')
                startPoint = index + 4
                creditsIndex = element.text.find(' credits')
                progressNumber = element.text[element.text.find('-') + 1:element.text.find(' of ')]
                totalNumber = element.text[startPoint:creditsIndex]
                self.desktopSearchMin = int(progressNumber)
                self.desktopSearchMax = int(totalNumber)
        if self.desktopSearchMin < self.desktopSearchMax:
            self.desktopDifference = self.desktopSearchMax - self.desktopSearchMin
            print "You need " + repr(self.desktopDifference) + " more desktop points"
        elif self.desktopSearchMin == self.desktopSearchMax:
            self.desktopDifference = 0
            print "You have all desktop searches today."


    def detect_offer_for_mobile(self):
        #Finds the multiplier for mobile searching
        #ie "1 point per 2 searches up to 30 a day"
        #multiplier == 2
        print "Detecting Mobile Offer"
        offers = self.browser.find_elements_by_class_name('offer')
        for offer in offers:
            offertitles = offer.find_elements_by_class_name('offertitle')
            for offertitle in offertitles:
                if offertitle.text.find('Mobile search-') > -1:
                    spans = offer.find_elements_by_xpath('div/a/div/span')
                    for span in spans:
                        if span.text.find('Earn 1 credit per ') > -1:
                            progressLength = len(offertitle.text)
                            progressIndex = offertitle.text.find(' of ')
                            progressStartPoint = progressIndex + 4
                            progressMin = offertitle.text[offertitle.text.find('-') + 1:offertitle.text.find(' of')]
                            progressMax = offertitle.text[progressStartPoint:progressLength]
                            multiplierLength = len(span.text)
                            multiplierStartPoint = span.text.find('per ') + 4
                            multiplier = span.text[multiplierStartPoint:multiplierStartPoint + 1]
                            self.mobileMultiplier = int(multiplier)
                            maxCreditsIndex = span.text.find('up to ') + 6
                            maxCredits = span.text[maxCreditsIndex:maxCreditsIndex + 2]
                            print "The multiplier is " + multiplier + " and max credits is " + maxCredits + " for Mobile searches"
                            print "I have " + progressMin + " out of " + progressMax + " for today."


    def detect_offer_for_desktop(self):
        #Finds the multiplier for desktop searching
        #ie "1 point per 2 searches up to 15 a day"
        #multiplier == 2
        print "Detecting Desktop Offer"
        offers = self.browser.find_elements_by_class_name('offer')
        for offer in offers:
            offertitles = offer.find_elements_by_class_name('offertitle')
            for offertitle in offertitles:
                if offertitle.text.find('PC search-') > -1:
                    spans = offer.find_elements_by_xpath('div/a/div/span')
                    for span in spans:
                        if span.text.find('Earn 1 credit per ') > -1:
                            progressLength = len(offertitle.text)
                            progressIndex = offertitle.text.find(' of ')
                            progressStartPoint = progressIndex + 4
                            progressMin = offertitle.text[offertitle.text.find('-') + 1:offertitle.text.find(' of')]
                            progressMax = offertitle.text[progressStartPoint:progressLength]
                            multiplierLength = len(span.text)
                            multiplierStartPoint = span.text.find('per ') + 4
                            multiplier = span.text[multiplierStartPoint:multiplierStartPoint + 1]
                            self.desktopMultiplier = int(multiplier)
                            maxCreditsIndex = span.text.find('up to ') + 6
                            maxCredits = span.text[maxCreditsIndex:maxCreditsIndex + 2]
                            print "The multiplier is " + multiplier + " and max credits is " + maxCredits + " for Desktop searches"
                            print "I have " + progressMin + " out of " + progressMax + " for today."

    def detect_and_claim_free_offer(self):
        #clicks on the "Earn 1 credit... offer available each day"
        offers = self.browser.find_elements_by_class_name('offer')
        for offer in offers:
            offertitles = offer.find_elements_by_class_name('offertitle')
            for offertitle in offertitles:
                if offertitle.text.find('Earn 1 credit') > -1:
                    print "Detecting and claiming free offer"
                    offertitle.click()
                    time.sleep(5)
                    return

    def description(self):
        return "Desktop [ " + repr(self.desktopSearchMin) + " / " + repr(self.desktopSearchMax) + " ] " + "Mobile [ " + repr(self.mobileSearchMin) + " / " + repr(self.mobileSearchMax) + " ] "


