import configparser
import os

from scrapy.crawler import CrawlerProcess
from scrapy.settings import SETTINGS_PRIORITIES
from scrapy.settings import Settings

from scrapy_get_events import AdventureEvents
from scrapy_get_lego import BrickSetSpider
from scrapy_get_etsy import EtsySpider
from scrapy_get_sashe import SasheSpider
from scrapy_get_generic import GenericSpider
from runner import GenericRunner

if not os.path.exists('conf/app.cfg'):
	print('App configuration missing! [conf/app.cfg]')
	exit(1)


def main():

    config = configparser.ConfigParser()
    config.read('conf/app.cfg')
    settings = Settings()
    settings.setmodule(config['DEFAULT'], priority=SETTINGS_PRIORITIES['spider'])
    process = CrawlerProcess(settings)
    #process.crawl(AdventureEvents)
    #process.crawl(BrickSetSpider)
    #process.crawl(EtsySpider)
    #process.crawl(SasheSpider)
    process.crawl(GenericSpider)
    process.start()

def test_runner_class():
    runner = GenericRunner()
    runner.scrape()

if __name__ == "__main__":
    #main()
    test_runner_class()