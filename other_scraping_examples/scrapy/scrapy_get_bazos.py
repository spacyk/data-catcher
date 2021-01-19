import re
from os import environ

import scrapy


class BazosSpider(scrapy.Spider):
    name = "bazos_spider"
    base_url = 'https://mobil.bazos.sk'
    start_urls = [
        f'{base_url}/apple/?hledat=iphone+x&rubriky=mobil&hlokalita=94911&humkreis=45&cenaod=&cenado=&kitx=ano',
        f'{base_url}/apple/?hledat=iphone+x&rubriky=mobil&hlokalita=81101&humkreis=45&cenaod=&cenado=&kitx=ano'
    ]
    page_number = 0

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': environ.get('SCRAPY_FEED_URI', ''),
        'DOWNLOAD_DELAY': 3,
        'AJAXCRAWL_ENABLED': True,
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED' : True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 50,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
        'AUTOTHROTTLE_DEBUG': False,

        'FEED_EXPORT_FIELDS': ['title', 'date', 'price', 'city', 'post', 'views', 'description', 'url']

    }

    def parse(self, response):
        self.page_number += 1

        SET_SELECTOR = '//table[@class="inzeraty"]'
        for product in response.xpath(SET_SELECTOR):

            #' img ::attr(src)'
            TITLE_SELECTOR = 'a ::text'
            DATE_SELECTOR = 'span.velikost10 ::text'
            PRICE_SELECTOR = 'span.cena ::text'
            CITY_SELECTOR = 'tbody tr td ::text'
            POST_SELECTOR = './/table/tbody/tr[1]/td[3]/text()'
            VIEWS_SELECTOR = '/html/body/div/table/tbody/tr/td[2]/span[1]/table/tbody/tr[1]/td[4]'
            DESCRIPTION_SELECTOR = 'div.popis ::text'
            URL_SELECTOR = 'a ::attr(href)'

            yield {
                'title': product.css(TITLE_SELECTOR).extract_first(),
                'date': (product.css(DATE_SELECTOR).extract())[-1].strip(' - [').strip(']'),
                'price': product.css(PRICE_SELECTOR).extract_first(),
                'city': product.css(CITY_SELECTOR).extract_first(),
                'post': product.xpath(POST_SELECTOR).extract_first(),
                'views': product.xpath(VIEWS_SELECTOR).extract_first(),
                'description': ''.join(product.css(DESCRIPTION_SELECTOR).extract()),
                'url': f'{self.base_url}{product.css(URL_SELECTOR).extract_first()}'
            }

        next_page = re.sub('\/\?', f'/{self.page_number * 20}/?', response.url)

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
