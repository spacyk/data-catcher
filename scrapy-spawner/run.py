from scrapy.crawler import CrawlerProcess
from scrapy.settings import SETTINGS_PRIORITIES
from scrapy.settings import Settings

import settings as module_settings

from scrapy_get_events import AdventureEvents
from scrapy_get_lego import BrickSetSpider
from scrapy_get_etsy import EtsySpider
from scrapy_get_sashe import SasheSpider


def main():
    settings = Settings()
    settings.setmodule(module_settings, priority=SETTINGS_PRIORITIES['spider'])
    process = CrawlerProcess(settings)
    #process.crawl(AdventureEvents)
    #process.crawl(BrickSetSpider)
    #process.crawl(EtsySpider)
    process.crawl(SasheSpider)
    process.start()

if __name__ == "__main__":
    main()