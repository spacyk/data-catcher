# coding: utf-8

import requests
from bs4 import BeautifulSoup

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.sqlite', echo=True)

Base = declarative_base(bind=engine)

class Shop(Base):
	__tablename__ = 'shops'
	id = Column(Integer, primary_key=True)
	name = Column(String(60))
	dresses = relationship('Dress')

class Dress(Base):
	__tablename__= 'dresses'
	id = Column(Integer, primary_key=True)
	brand = Column(String(30))
	name = Column(String(120))
	price = Column(Float)
	shop_id = Column(Integer, ForeignKey('shops.id'))

	def __repr__(self):
		return f'{self.id}, {self.brand}, {self.name}, {self.price}, {self.shop_id}'

#Base.metadata.create_all()


def get_zoot_dresses():
	Session = sessionmaker(bind=engine)
	session = Session()

	response = requests.get('https://www.zoot.sk/kategoria/22911/zeny/saty/')
	soup = BeautifulSoup(response.content, 'html.parser')
	content = soup.find_all('article', class_='js-productList__items productList__items productList__items--hasHoverImg')

	shop = Shop(name='Zoot')
	session.add(shop)
	session.commit()
	for dress in content:
		brand = dress.find(class_='productList__brand').text
		name = dress.find(class_='productList__name').text
		price = float(dress.find(class_='productList__priceBox__item').text.split()[0].replace(',', '.'))

		dress = Dress(brand=brand, name=name, price=price, shop_id=shop.id)
		session.add(dress)

	session.commit()
	session.close()

def filter_with_bigger_price(price=30):
	Session = sessionmaker(bind=engine)
	session = Session()

	dresses = session.query(Dress).filter(Dress.price >= price)
	for dress in dresses:
		print(str(dress))

	shop = session.query(Shop).filter(Shop.name == 'Zoot')[0]
	dresses = session.query(Dress).filter(Dress.shop_id == shop.id)
	for dress in dresses:
		print(str(dress))

	session.close()


#get_zoot_dresses()
filter_with_bigger_price()



