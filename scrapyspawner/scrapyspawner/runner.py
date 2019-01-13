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

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('conf/app.cfg')
        self.settings = Settings()
        self.settings.setmodule(self.config['DEFAULT'], priority=SETTINGS_PRIORITIES['spider'])
        self.process = CrawlerProcess(self.settings)

    def scrape(self):
        url = 'https://www.zoot.sk/kategoria/22911/zeny/saty/'
        page_changing_string = 'stranka/'
        xpath_element_definition = '//article[@class="js-productList__items productList__items productList__items--hasHoverImg"]'
        self.process.crawl(
            GenericSpider, url, page_changing_string, xpath_element_definition
        )
        self.process.start()
