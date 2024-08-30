import logging

import requests
from bs4 import BeautifulSoup
from mongoengine import NotUniqueError
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from models import Author, Quote
from connect import connect

BASE_URL = 'https://quotes.toscrape.com'


def parse_quotes(quote_list, this_page_url='/'):
    current_url = BASE_URL + this_page_url[:-1]
    response = requests.get(current_url)
    print(response.status_code)
    my_html = response.text
    soup = BeautifulSoup(my_html, 'lxml')
    quotes_info = soup.find_all('div', class_='quote')
    for quote_info in quotes_info:
        quote = quote_info.find('span', class_='text').text
        author = quote_info.find('small', class_='author').text
        tags = quote_info.find_all('a', class_='tag')
        tags_ = list()
        for tag in tags:
            tags_.append(tag.text)
        quote_list.append({'quote': quote, 'author': author, 'tags': tags_})

        authors_link = quote_info.find('a')['href']
        parse_author(author, BASE_URL + authors_link)
        author_obj = Author.objects(fullname=author).first()
        author_oid = author_obj.id
        try:
            Quote(quote=quote, author=author_oid, tags=tags_).save()
        except NotUniqueError as err:
            print(f'{err}')

    next_page_tag = soup.find('li', class_='next')

    if next_page_tag:
        next_page_link = next_page_tag.find('a')['href']
        print(next_page_link)
        parse_quotes(quote_list, next_page_link)
    return quote_list


def parse_author(author_name: str, author_url: str):
    resource = requests.get(author_url)
    html = resource.text
    soup = BeautifulSoup(html, 'lxml')
    author_details = soup.find('div', class_='author-details')
    author_born_date = author_details.find('span', class_='author-born-date').text
    author_born_location = author_details.find('span', class_='author-born-location').text
    author_description = author_details.find('div', class_='author-description').text
    try:
        Author(fullname=author_name, born_date=author_born_date,
               born_location=author_born_location, description=author_description).save()
    except NotUniqueError as err:
        print(f'{err}')


if __name__ == '__main__':
    print('start')
    quotes_all_info = list()
    parse_quotes(quotes_all_info)
