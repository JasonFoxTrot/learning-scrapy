import scrapy
import re


class CoolblueSpider(scrapy.Spider):
    name = "coolblue_prices"
    start_urls = [
    ]

    with open('urls.txt', 'r') as file:
        for line in file:
            start_urls.append(line)

    def parse(self, response):
        selector = "div.grid-unit-xs--col-12"

        for product in response.css(selector):
            if product.css('span.sales-price__former').extract_first():

                url = product.css('div.product__titles a.js-product-title::attr(href)').extract_first()

                if url[:5] != 'https':
                    url = response.url + url

                price = product.css('span.sales-price__former::text').extract_first()
                price = re.sub('[^0-9\,\-]', '', price)

                if ',-' in price:
                    price = price[:-2]

                promotional_price = product.css('strong.sales-price__current::text').extract_first()
                promotional_price = re.sub('[^0-9\,-]', '', promotional_price)

                if ',-' in promotional_price:
                    promotional_price = promotional_price[:-2]

            elif product.css('div.product__titles a.js-product-title::attr(href)').extract_first() and product.css(
                    'strong.sales-price__current::text').extract_first():

                url = product.css('div.product__titles a.js-product-title::attr(href)').extract_first()

                if url[:5] != 'https':
                    url = response.url + url

                price = product.css('strong.sales-price__current::text').extract_first()
                price = re.sub('[^0-9\,\-]', '', price)

                if ',-' in price:
                    price = price[:-2]

                promotional_price = "NaN"

            yield {
                'url': url,
                'price': price,
                'promotional_price': promotional_price
            }

        next_page = response.url.split('?')[0] + response.xpath('//li[@class="pagination__item '
                                                                'pagination__item--active"]/following-sibling::*/a'
                                                                '/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
