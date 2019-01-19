import logging

import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic_spider"
    page_number = 0
    products_list = []

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/generic_output.csv',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY': 3,
        'AJAXCRAWL_ENABLED': True,
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED' : True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 50,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
        'AUTOTHROTTLE_DEBUG': False
    }

    def __init__(self, url='', page_changing_string='', xpath_element_definition=''):
        super().__init__(start_urls=[url])
        self.page_changing_string = page_changing_string
        self.xpath_element_definition = xpath_element_definition


    def parse(self, response):

        self.find_products_list(response)
        if not self.products_list:
            raise ElementsNotFound

        for product_data in self.get_products_data():
            yield product_data

        self.page_number += 1
        next_page = f'{self.start_urls[0]}{self.page_changing_string}{self.page_number*20}/'
        logging.info(f'Scraping page: {self.page_number}')
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def find_products_list(self, response):
        self.products_list = response.xpath(self.xpath_element_definition)


    def get_products_data(self):
        for product_context in self.products_list:
            cleared_attribs = [attrib.strip() for attrib in product_context.xpath('.//node()/text()').extract()]
            relevant_attribs = [attrib for attrib in cleared_attribs if attrib]
            if not relevant_attribs:
                continue
            yield {
                f'field_{index}': value for index, value in enumerate(relevant_attribs)
            }


class ElementsNotFound(Exception):
    """Your xpath defined elements were not found on the page"""