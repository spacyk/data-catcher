import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://www.slevomat.cz/praha/zabava-a-volny-cas/adrenalinove-zazitky']
    page_number = 1


    def parse(self, response):
        self.page_number += 1
        SET_SELECTOR = '.product'
        set = response.css(SET_SELECTOR)
        if not set:
            return
        for brickset in set:
            NAME_SELECTOR = 'h3 ::text'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
            }

            next_page = f'{self.start_urls[0]}?page={self.page_number}'

            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )