import urllib2
from faker import Faker
from random import randint

class QueryGenerator(object):
    def __init__(self):
        self.hello = "Query Generator"

    def generate_search_string(self):
        number = randint(0,5)
        if number == 0:
            string = self.quote()
        elif number == 1:
            string = self.name()
        elif number == 2:
            string = self.username()
        elif number == 3:
            string = self.email()
        elif number == 4:
            string = self.company()
        elif number == 5:
            string = self.phone()
        return string


    def quote(self):
        quote = urllib2.urlopen("http://www.iheartquotes.com/api/v1/random?max_lines=1&show_permalink=false&show_source=false").read()
        return quote.decode('utf8')

    def name(self):
        f = Faker()
        string = f.name()
        return string.decode('utf8')

    def email(self):
        f = Faker()
        string = f.email()
        return string.decode('utf8')

    def phone(self):
        f = Faker()
        string = f.phonenumber()
        return string.decode('utf8')

    def username(self):
        f = Faker()
        string = f.username()
        return string.decode('utf8')

    def company(self):
        f = Faker()
        string = f.company()
        return string.decode('utf8')