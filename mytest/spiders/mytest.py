import scrapy
from mytest.items import MyItem


class MytestSpider(scrapy.Spider):
    name = "mytest"
    allowed_domains = ["eastbay.com"]

    start_urls = [
        "https://www.eastbay.com/category/sale.html?query=sale%3Arelevance%3AstyleDiscountPercent%3ASALE%3Agender%3AMen%27s%3Abrand%3AASICS+Tiger"
    ]

    def parse(self, response):

        hrefs = []
        for sel in response.xpath(
                '//*[@id="main"]/div/div[2]/div/section/div/div[2]/ul/li'):
            hrefs.append(sel.xpath('div/a//@href')[0].extract())
            for href in hrefs:
                yield scrapy.Request(url='https://www.eastbay.com' + href,
                                     callback=self.href_parse)
    def href_parse(self, response):
        item = MyItem()
        item['title'] = response.xpath(
            '//*[@id="pageTitle"]/span/span[1]/text()')[0].extract()

        item['price'] = response.xpath(
            '//*[@id="ProductDetails"]/div[5]/div[1]/span/div/p/span[1]/text()')[0].extract()

        item['color'] = response.xpath(
            '//*[@id="ProductDetails"]/div[5]/p[1]/text()')[0].extract()

        sizes=[]
        size_divs=response.xpath('//*[@id="ProductDetails"]/div[5]/div[2]/fieldset/div/div')
        for div in size_divs:
            sizes.append(div.xpath('label/span/text()')[0].extract())
        item['size'] = sizes

        item['sku'] = response.xpath('//*[@id="ProductDetails"]/div[3]/fieldset/div[1]/label/span/span/img//@id')[0].extract()

        item['details'] = response.xpath('//*[@id="ProductDetails-tabs-details-panel"]').xpath('string(.)')[0].extract()

        item['URL'] = response.xpath(
            '//*[@id="main"]/div/div[2]/div/section/div[2]/div/div/div/div/span/img//@src')[0].extract()
         
        yield item
