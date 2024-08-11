import scrapy
from scrapy.crawler import CrawlerProcess
from pathlib import Path
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        json_file = Path('quotes.json')
        if not json_file.is_file():
            data = []
            with open(json_file, 'w') as file:
                json.dump(data, file)

        with open(json_file, 'r') as file:
            existing_json_file = json.load(file)

        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("//small[@itemprop='author']/text()").get()
            quote = quote.xpath("span[@class='text']/text()").get()

            quote_item = {'tags': tags, 'author': author, 'quote': quote}

            if quote_item not in existing_json_file:
                print(quote_item)
                existing_json_file.append(quote_item)

        with open(json_file, 'w') as file:
            json.dump(existing_json_file, file, indent=4, ensure_ascii=False)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
