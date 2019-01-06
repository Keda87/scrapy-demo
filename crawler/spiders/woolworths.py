import scrapy
from scrapy import Selector
from scrapy_splash import SplashRequest


class BlogSpider(scrapy.Spider):
    name = 'woolworths'
    url = 'https://www.woolworths.com.au'

    def start_requests(self):
        yield SplashRequest(
            self.url,
            self.parse,
            endpoint='render.html',
            args={'wait': 0.5},
        )

    def parse_detail_product(self, response):
        return

    def parse_product(self, response):
        products = response.css('a.shelfProductTile-descriptionLink')
        for product in products:
            print(product.attrib.get('href'))

    def parse_menu(self, response):
        side_menus = response.css('li a.categoriesNavigation-link')
        for side_menu in side_menus:
            yield SplashRequest(
                f'{self.url}{side_menu.attrib.get("href")}',
                self.parse_product,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        navigation = response.css('nav.categoryHeader-navigation._departmentNav').extract_first()
        menus = Selector(text=navigation).xpath('//a[@class="categoryHeader-navigationLink"]')
        for menu in menus:
            yield SplashRequest(
                f'{self.url}{menu.attrib.get("href")}',
                self.parse_menu,
                endpoint='render.html',
                args={'wait': 0.5},
            )
