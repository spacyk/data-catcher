import os

from scrapy.crawler import CrawlerProcess

from scrapy_get_generic import GenericSpider


class GenericRunner:

    def __init__(self, url='', page_changing_string='', xpath_element_definition=''):
        if not all([url, xpath_element_definition]):
            raise ValueError("One of the mandatory arguments is not specified")
        self.url = url
        self.page_changing_string = page_changing_string
        self.xpath_element_definition = xpath_element_definition
        self.process = CrawlerProcess()

    def scrape(self):
        self.process.crawl(
            GenericSpider, url=self.url, page_changing_string=self.page_changing_string, xpath_element_definition=self.xpath_element_definition
        )
        self.process.start()
