import configparser
import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import SETTINGS_PRIORITIES
from scrapy.settings import Settings

from scrapy_get_generic import GenericSpider

if not os.path.exists('conf/app.cfg'):
    print('App configuration missing! [conf/app.cfg]')
    exit(1)


class GenericRunner:

    def __init__(self, url='', page_changing_string='', xpath_element_definition=''):
        if not all([url, xpath_element_definition]):
            raise ValueError("One of the mandatory arguments is not specified")
        self.url = url
        self.page_changing_string = page_changing_string
        self.xpath_element_definition = xpath_element_definition
        self.config = configparser.ConfigParser()
        self.config.read('conf/app.cfg')
        self.settings = Settings()
        self.settings.setmodule(self.config['DEFAULT'], priority=SETTINGS_PRIORITIES['spider'])
        self.process = CrawlerProcess(self.settings)

    def scrape(self):
        self.process.crawl(
            GenericSpider, url=self.url, page_changing_string=self.page_changing_string, xpath_element_definition=self.xpath_element_definition
        )
        self.process.start()
