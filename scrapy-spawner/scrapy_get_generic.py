import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic_spider"
    start_urls = ['https://www.sashe.sk/handmade/prstene-pevne_____']
    #start_urls = ['https://www.etsy.com/c/jewelry-and-accessories?explicit=1&min=&max=500&price_bucket=1&free_shipping=true&locationQuery=3077311']
    #start_urls = ['https://www.slevomat.cz/praha/zabava-a-volny-cas/adrenalinove-zazitky']
    page_number = 1
    prepared = False
    SET_SELECTOR = None
    products_list = None

    custom_settings = {
        'FEED_URI': '/home/spacyk/Projects/data-catcher/test_generic.csv',
    }

    def parse(self, response):
        self.page_number += 1

        body = '/html/body//node()'
        all_nested_nodes = response.xpath(body)

        potential_elements_counter = 0
        for nested_node in all_nested_nodes:
            product_elements = nested_node.xpath('./node()')
            if len(product_elements) > 20:
                potential_elements_counter += 1
                # this needs to be solved so we can find the important list
                #self.content = a if len(a.extract()) > len(self.content) else self.content
                self.products_list = product_elements
                #print(len(a.extract()))
                #print(a.extract())
            print(potential_elements_counter)
            print(self.products_list)
            yield scrapy.Request(
                response.urljoin(self.start_urls[0]),
                callback=self.parse
            )

        for product_data in self.get_products_data():
            yield product_data

        next_page = f'{self.start_urls[0]}?p={self.page_number}'
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def get_products_data(self):
        for product_context in self.products_list:
            # This could be usefull for some cases
            # atribs = brickset.xpath('.//node()/@*').extract()
            texts = [attrib.strip() for attrib in product_context.xpath('.//node()/text()').extract()]
            if not texts:
                continue
            yield {
                f'field_{index}': value for index, value in enumerate(texts[:5])
            }
