from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()

for n in range(1,9001):
	
	r = session.get('https://auto.ria.com/legkovie/?page=' + str(n)).text
	soup = BeautifulSoup(r, 'lxml')
	for section in soup.find_all('section', class_="ticket-item new__ticket t paid"):
			mark = section.find('div')['data-mark-name']
			model = section.find('div')['data-model-name']
			price = section.find('div', class_="price-ticket")['data-main-price']
			mileage = section.find('li', class_="item-char").text
			print(mark + "," + model + "," + price + "," + mileage)
	n += 1