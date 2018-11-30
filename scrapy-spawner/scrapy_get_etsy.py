import scrapy


class EtsySpider(scrapy.Spider):
    name = "etsy_spider"
    start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?explicit=1&min=&max=500&price_bucket=1&free_shipping=true&locationQuery=3077311']
    page_number = 1

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/test_etsy.csv',
        'FEED_EXPORT_FIELDS': ['name', 'price']
    }

    def parse(self, response):
        self.page_number += 1
        SET_SELECTOR = '//*[@id="reorderable-listing-results"]/li'
        for brickset in response.xpath(SET_SELECTOR):

            NAME_SELECTOR = './/div/a/div[2]/div/p[1]/text()'
            PRICE_SELECTOR = './/div/a[1]/div[2]/div/p[2]/span[@class="currency-value"]/text()'
            yield {
                'name': brickset.xpath(NAME_SELECTOR).extract_first(),
                'price': brickset.xpath(PRICE_SELECTOR).extract_first()
            }

        next_page = f'{self.start_urls[0]}&page={self.page_number}'

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
