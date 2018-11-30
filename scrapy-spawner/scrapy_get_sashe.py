import scrapy


class SasheSpider(scrapy.Spider):
    name = "sashe_spider"
    start_urls = ['https://www.sashe.sk/handmade/prstene-pevne_____']
    page_number = 1

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/test_sashe.csv',
        'FEED_EXPORT_FIELDS': ['name', 'price']
    }

    def parse(self, response):
        self.page_number += 1

        SET_SELECTOR = '//*[@id="seller-list"]/div'
        for brickset in response.xpath(SET_SELECTOR):

            NAME_SELECTOR = './/div/div[3]/text()'
            PRICE_SELECTOR = './/div/div[2]/text()'
            yield {
                'name': brickset.xpath(NAME_SELECTOR).extract_first(),
                'price': brickset.xpath(PRICE_SELECTOR).extract_first()
            }

        next_page = f'{self.start_urls[0]}?p={self.page_number}'

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
