import scrapy
import hashlib
from bs4 import BeautifulSoup
from database import Database


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def __init__(self):
        self.database = Database()

    def start_requests(self):
        urls = [
            'http://www.politico.com/2016-election/results/map/president/florida/',
            'http://www.politico.com/2016-election/results/map/president/pennsylvania/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'states-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        soup = BeautifulSoup(response.body, 'html.parser')
        year = response.url.split("/")[3]
        newYear = year.split("-")[0]
        print(newYear)
        for article in soup.find_all('article'):
            # print(len(list(articles)))
            self.parseArticle(article, page, newYear)


    def parseArticle(self, articles, state, year):
        if articles.get('id') != None:
            #print(articles.select('.type-democrat .results-popular'))
            democratPopularResult = articles.select('.type-democrat .results-popular')
            print(len(democratPopularResult))
            if (len(democratPopularResult) > 0):
                newResult = democratPopularResult[0].string.replace(",", "")
                #print(int(newResult))
                counties = articles.select('h4')
                newCounties = counties[0].string
                party = "democrat"
                dbObject = {
                    "state": state,
                    "year": year,
                    "newCounties": newCounties,
                    "party": party,
                    "result": int(newResult)
                }
                print(dbObject)

                uniqueId = state + year + newCounties + party
                print(uniqueId)

                m = hashlib.md5()
                m.update(uniqueId)
                newId = m.hexdigest()
                print(newId)

                #print(newCounties)
                # votes = {
                #    "democrat": democratPopularResult
                # }
                self.database.set(newId, dbObject)
