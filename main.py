import logging
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from pathlib import Path
import json

from connect import connect
from models import Author, Quote


def save_item(data_to_save: dict, file_path: Path):
    if not file_path.is_file():
        data = []
        with open(file_path, 'w') as file:
            json.dump(data, file)

    with open(file_path, 'r') as file:
        existing_json_file = json.load(file)

    if data_to_save not in existing_json_file:
        existing_json_file.append(data_to_save)

    with open(file_path, 'w') as file:
        json.dump(existing_json_file, file, indent=4, ensure_ascii=False)


def send_quote_to_db(quote: dict):
    tags = quote['tags']
    author = quote['author']
    a_quote = quote['quote']

    all_quotes = Quote.objects().all()
    if a_quote not in [db_quote.quote for db_quote in all_quotes]:
        Quote(tags=tags, author=author, quote=a_quote).save()


def send_author_to_db(author: dict):
    fullname = author['fullname']
    born_date = author['born_date']
    born_location = author['born_location']
    description = author['description']

    all_authors = Author.objects().all()
    if fullname not in [db_author.fullname for db_author in all_authors]:
        Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()


class QuotesSpider(scrapy.Spider):
    try:
        os.remove(Path('quotes.json'))
        os.remove(Path('authors.json'))
    except FileNotFoundError as err:
        logging.debug(err)

    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quotes_path = Path('quotes.json')
        for quote in response.xpath("/html//div[@class='quote']"):
            author_link = self.start_urls[0] + quote.xpath("span/a/@href").get()
            scrapy.Request(url=author_link, callback=self.parse_authors)

            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            authors_name = quote.xpath("span/small[@itemprop='author']/text()").get()
            author = Author.objects(fullname=authors_name).first()
            print(author, '<---->')
            a_quote = quote.xpath("span[@class='text']/text()").get()

            quote_item = {'tags': tags, 'author': author.id, 'quote': a_quote}
            send_quote_to_db(quote_item)
            save_item(quote_item, quotes_path)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_authors(self, response):
        authors_path = Path('authors.json')

        fullname = response.xpath("/html//h3[@class='author-title']/text()").get()
        born_date = response.xpath("/html//span[@class='author-born-date']/text()").get()
        born_location = response.xpath("/html//span[@class='author-born-location']/text()").get()
        description = response.xpath("/html//div[@class='author-description']/text()").get()[9:]

        author_item = {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }
        save_item(author_item, authors_path)
        send_author_to_db(author_item)


# run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
