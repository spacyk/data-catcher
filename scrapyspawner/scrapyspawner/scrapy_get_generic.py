import logging

import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic_spider"
    #start_urls = ['https://www.sashe.sk/handmade/prstene-pevne_____tepanie']
    #start_urls = ['https://www.etsy.com/c/handmade/jewelry-and-accessories?explicit=1&min=200&max=300&free_shipping=true&locationQuery=3077311']
    #start_urls = ['https://www.slevomat.cz/praha/zabava-a-volny-cas/adrenalinove-zazitky']
    #start_urls = ['https://mobil.bazos.cz/apple/']
    start_urls = ['https://www.zoot.sk/kategoria/22911/zeny/saty/']
    page_number = 1
    prepared = False
    SET_SELECTOR = None
    products_list = []

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/test_generic.csv',
    }

    def parse(self, response):

        self.find_products_list(response)

        if not self.products_list:
            return
        for product_data in self.get_products_data():
            yield product_data

        self.page_number += 1
        next_page = f'{self.start_urls[0]}stranka/{self.page_number}'
        logging.info(f'Scraping page: {self.page_number}')
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def find_products_list(self, response):
        '''
        body = '/html/body//node()'
        all_nested_nodes = response.xpath(body)

        potential_elements_counter = 0
        for nested_node in all_nested_nodes:
            product_elements = nested_node.xpath('./node()')
            if len(product_elements) > 20:
                potential_elements_counter += 1
                # this needs to be solved so we can find the important list
                #self.content = a if len(a.extract()) > len(self.content) else self.content
                if potential_elements_counter == 5:
                    self.products_list = product_elements
                #print(len(a.extract()))
                #print(a.extract())
            #print(potential_elements_counter)
            #print(self.products_list)
        '''

        #SELECTOR = '//*[@id="seller-list"]/div' #SASHE working
        #SELECTOR = '//*[@id="reorderable-listing-results"]/li' #ETSY no wokring on 2nd page
        #SELECTOR = '//*[@class="product"]' #ZLAVOMAT working
        #SELECTOR = '//table[@class="inzeraty"]' #BAZOS working
        SELECTOR = '//article[@class="js-productList__items productList__items productList__items--hasHoverImg"]' #ZOOT working
        self.products_list = response.xpath(SELECTOR)


    def get_products_data(self):
        for product_context in self.products_list:
            # This could be usefull for some cases
            # atribs = brickset.xpath('.//node()/@*').extract()
            cleared_attribs = [attrib.strip() for attrib in product_context.xpath('.//node()/text()').extract()]
            relevant_attribs = [attrib for attrib in cleared_attribs if attrib]
            if not relevant_attribs:
                continue
            yield {
                f'field_{index}': value for index, value in enumerate(relevant_attribs)
            }
