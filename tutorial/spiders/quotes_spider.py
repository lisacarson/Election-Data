import scrapy
from bs4 import BeautifulSoup



class QuotesSpider(scrapy.Spider):
    name = "quotes"

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
        for article in soup.find_all('article'):
            # print(len(list(articles)))
            self.parseArticle(article)

    def parseArticle(self, articles):
        if articles.get('id') != None:
            print(articles.select('.type-democrat .results-popular'))
