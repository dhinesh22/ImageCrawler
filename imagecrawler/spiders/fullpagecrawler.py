import scrapy
import re
from ..items import FullpagecrawlerItem


class ScrapyTutSpider(scrapy.Spider):
    name = "webbot"
    page_number = 2
    start_urls = [
        'https://www.loopnet.com/for-sale/san-francisco-ca/retail-properties/'
    ]

    def parse(self, response):
        containers = response.css("article.placard.tier4")
        for container in containers:
            url_links = container.css("h4 a::attr(href)").extract()
            url_str = url_links[0]
            yield response.follow(url_str, callback=self.parse_page)


        next_page = "https://www.loopnet.com/for-sale/san-francisco-ca/retail-properties/" + str(
            ScrapyTutSpider.page_number) + ""
        if ScrapyTutSpider.page_number <= 2:
            ScrapyTutSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        items = FullpagecrawlerItem()
        a = []
        result = []
        pattern = '[^A-Za-z0-9]+'
        values = response.css(".featured-grid td")
        for val in values:
            off1 = val.css("td::text").extract_first()
            off2 = val.css("td span::text").extract()
            off1 = re.sub(pattern, "", str(off1))
            off1.strip()
            a.append(off1)
            if off2:
                temp = a + off2
                dump = temp[0] + "::" + temp[2]
                dump = str(dump)
                result.append(dump)
                a = []
        items['offering'] = result
        yield items
