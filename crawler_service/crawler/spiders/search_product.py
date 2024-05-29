import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
from crawler.items import ProductItem
from module import generator_url_module, search_product_module, get_config_module


class SearchProduct(scrapy.Spider):
    name = 'search_product'
    urls = generator_url_module.get_search_url()
    if not urls:
        raise Exception("can not get urls")

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 9_13_9) AppleWebKit/613.19.89 (KHTML, like Gecko) Version/10.8.1 Safari/611.7.12'
        }

        for url in self.urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 1, 'headers': headers})

    def parse(self, response):
        products = response.xpath(
            "//div[@data-testid[starts-with(., 'listing-card-') and substring-after(., 'listing-card-') = translate(substring-after(., 'listing-card-'), ' ', '')]]")
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        for product in products:
            ProductItem()

            yield {
                'seller_id': product.xpath(".//p[@data-testid='listing-card-text-seller-name']/text()").extract_first(
                    default=""),
                'product_link': get_config_module.carousell_url + search_product_module.parse_url(
                    product.xpath(".//a[starts-with(@href, '/p')]/@href").extract_first(default="")),
                'product_name': product.xpath(".//img[contains(@src, 'products')]/@title").extract_first(default=""),
                'price': product.xpath(".//p[@title[starts-with(., 'NT$')]]/text()").extract_first(default=""),
                'product_add_at': search_product_module.date_format(
                    product.xpath(".//div[1]/a[1]/div[2]/div/p/text()").extract_first(default="")),
                'product_add_since': product.xpath(".//div[1]/a[1]/div[2]/div/p/text()").extract_first(default=""),
                'created_at': timestamp
            }