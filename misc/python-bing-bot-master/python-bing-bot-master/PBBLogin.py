from selenium import webdriver
import yaml
import time
class Login(object):
    def __init__(self, withBrowser):
        self.browser = withBrowser

    def login_to_facebook(self,accountInfo):
        self.browser.get("http://www.facebook.com")
        time.sleep(5)
        emailField = self.browser.find_element_by_name('email')
        username = accountInfo[0]
        password = accountInfo[1]
        print "Logging in to Facebook with " + username
        emailField.send_keys(username)
        passwordField = self.browser.find_element_by_name('pass')
        passwordField.send_keys(password)
        passwordField.submit()

    def login_to_outlook(self,accountInfo):
        self.browser.get("http://outlook.com")
        time.sleep(5)
        username = accountInfo[0]
        password = accountInfo[1]
        print "Logging in to Outlook with " + username
        emailField = self.browser.find_element_by_name('login')
        emailField.send_keys(username)
        passwordField = self.browser.find_element_by_name('passwd')
        passwordField.send_keys(password)
        passwordField.submit()

    def logout_from_bing(self):
        self.browser.get('http://www.bing.com')
        time.sleep(5)
        print "Logging out"
        self.browser.find_element_by_id('id_l').click()
        time.sleep(5)
        self.browser.find_element_by_partial_link_text('Sign out').click()
        time.sleep(5)

    def logout_from_mobile_bing(self):
        print "Logging out mobile"
        self.browser.get('http://www.bing.com/rewards/dashboard')
        time.sleep(5)
        self.browser.find_element_by_xpath('//*[@id="mbHeader"]/a[2]/img').click()
        time.sleep(5)
        self.browser.find_element_by_xpath('//*[@id="Account"]').click()
        time.sleep(5)
        self.browser.find_element_by_partial_link_text('Sign out').click()
        time.sleep(5)

