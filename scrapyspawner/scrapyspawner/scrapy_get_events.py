import scrapy


class AdventureEvents(scrapy.Spider):
    name = "adventures_spider"
    start_urls = ['https://www.slevomat.cz/praha/zabava-a-volny-cas/adrenalinove-zazitky']
    page_number = 1

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/test_events.csv',
        'FEED_EXPORT_FIELDS': ['name', 'webpage', 'email', 'phone', 'rating', 'ratings_number']
    }

    def parse(self, response):
        self.page_number += 1
        SET_SELECTOR = '.product'
        set = response.css(SET_SELECTOR)
        if not set:
            return
        for brickset in set:
            ADDRESS_SELECTOR = 'a ::attr(href)'
            element_address = brickset.css(ADDRESS_SELECTOR).extract_first(),
            yield scrapy.Request(
                response.urljoin(element_address[0]),
                callback=self.parse_content_page
            )
            next_page = f'{self.start_urls[0]}?page={self.page_number}'


            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )


    def parse_content_page(self, response):
        NAME_SELECTOR = 'h1 ::text'
        WEBPAGE_SELECTOR = '//*[@id="o-podniku"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/a/text()'
        EMAIL_SELECTOR = '//*[@id="o-podniku"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/a/text()'
        PHONE_SELECTOR = '//*[@id="o-podniku"]/div/div[2]/div[1]/div[2]/div[2]/div[3]/a/text()'
        RATING_SELECTOR = '//*[@id="layout"]/div[2]/div[1]/div[1]/div[3]/div/div/div[4]/div[2]/div[2]/div[3]/a/span/text()'
        RATINGS_NUMBER_SELECTOR = '//*[@id="layout"]/div[2]/div[1]/div[1]/div[3]/div/div/div[4]/div[2]/div[2]/div[3]/span/a/text()'
        ratings_number_text = response.xpath(RATINGS_NUMBER_SELECTOR).extract_first()
        ratings_number = ratings_number_text.split(' ')[0] if ratings_number_text else None
        yield {
            'name': response.css(NAME_SELECTOR).extract_first(),
            'webpage': response.xpath(WEBPAGE_SELECTOR).extract_first(),
            'email': response.xpath(EMAIL_SELECTOR).extract_first(),
            'phone': response.xpath(PHONE_SELECTOR).extract_first(),
            'rating': response.xpath(RATING_SELECTOR).extract_first(),
            'ratings_number': ratings_number,
            'page_number': self.page_number
        }
