from bs4 import BeautifulSoup
from requests_html import HTMLSession
import csv
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

filename = 'car-scribeOTO_' + timestr + '.csv'
session = HTMLSession()

with open(filename, 'w', newline='\n', encoding='utf-8') as f:
    fieldnames = ['id', 'make', 'link', 'title', 'comment',
                  'year', 'mileage', 'engine_capacity', 'fuel_type', 'price']
    thewriter = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
    thewriter.writeheader()
for n in range(1, 500):
    r = session.get(
        'https://www.otomoto.pl/osobowe/?search%5Border%5D=created_at%3Adesc&page=' + str(n)).text
    soup = BeautifulSoup(r, 'lxml')
    """ for section in soup.find_all('div', class_="offers list"):
            id = section.find('article')['data-ad-id']
            make = section.find('article')['data-param-make']
            link = section.find('article')['data-href']
            title = section.find('a', class_="offer-title__link")['title']
            comment = section.find('a')['title']
            year = section.find(attrs={"data-code": "year"}).text.strip()
            mileage = section.find(attrs={"data-code": "mileage"}).text.strip()[0:-3]
            engine_capacity = section.find(attrs={"data-code": "engine_capacity"}).text.strip()[0:-4]
            fuel_type = section.find(attrs={"data-code": "fuel_type"}).text.strip()
            price = section.find('div', class_="price-wrapper-listing").text.strip()[0:-4]
            city = section.find('h4', class_="ds-location hidden-xs").text.strip() """

    for offer in soup.find_all('article'):
        offer_id = offer.find('a')['data-ad-id']
        make = offer.find('a')['href'].split('/')[4]
        make = make.split('-')[0]
        link = offer.find('a')['href']
        title = offer.find('a', class_="offer-title__link")['title']
        try:
            comment = offer.find('div', class_="offer-item__title").h3.text
            comment = str(comment)
        except AttributeError:
            comment = 'None'
        year = offer.find(attrs={"data-code": "year"}).text.strip()
        try:
            mileage = offer.find(
                attrs={"data-code": "mileage"}).text.strip()[0:-3]
            mileage = mileage.replace(' ', '')
        except AttributeError:
            mileage = 0
        try:
            engine_capacity = offer.find(
                attrs={"data-code": "engine_capacity"}).text.strip()[0:-4]
            engine_capacity = engine_capacity.replace(' ', '')
        except AttributeError:
            engine_capacity = 0
        fuel_type = offer.find(attrs={"data-code": "fuel_type"}).text.strip()
        try:
            price = offer.find(
                'span', class_="offer-price__number ds-price-number").text.strip()[0:-4].replace(',', '.')
            price = price.replace(' ', '')
        except AttributeError:
            price = 0
        #city = offer.find('h4', class_="ds-location hidden-xs").text.strip()
        #city = city.split(' ')[0]
        with open(filename, 'a', newline='\n', encoding='utf-8') as f1:
            fieldnames = ['id', 'make', 'link', 'title', 'comment',
                    'year', 'mileage', 'engine_capacity', 'fuel_type', 'price']
            thewriter = csv.DictWriter(
                f1, fieldnames=fieldnames, delimiter='|')
            thewriter.writerow({'id': offer_id, 'make': make, 'link': link, 'title': title, 'comment': comment, 'year': year,
                                'mileage': mileage, 'engine_capacity': engine_capacity, 'fuel_type': fuel_type, 'price': price})

    print(offer_id, link, title, comment, year,
        mileage, engine_capacity, fuel_type, price)

    n += 1
