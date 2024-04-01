import scrapy
from scrapy.crawler import CrawlerProcess
import json
import time
result_quotes = []
result_authors = []
class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    def parse(self, response):
        
        for quote in response.xpath("/html//div[@class='quote']"):
            result = {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
            author = quote.xpath("span/a/@href").get()
            
            if author:
                yield scrapy.Request(url=self.start_urls[0] + author, callback=self.parser_author_page)  
            result_quotes.append(result)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        with open ('quotes.json', 'w', encoding='utf-8') as qfile:
            json.dump(result_quotes,qfile, indent=1,ensure_ascii=False)        
       
        with open ('authors.json', 'w', encoding='utf-8') as afile:
            json.dump(result_authors,afile,indent=1,ensure_ascii=False)
    
    def parser_author_page(self,response):
        #print(response)
        author_details = response.xpath("/html//div[@class='author-details']")
        
        result = {
            'fullname': author_details.xpath("h3[@class='author-title']/text()").get(),
            'born_date:': author_details.xpath("p/span[@class='author-born-date']/text()").get(),
            'born_location':author_details.xpath("p/span[@class='author-born-location']/text()").get(),
            'desctiption': author_details.xpath("div[@class='author-description']/text()").get()
        }
        result_authors.append(result)

        
       
# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()