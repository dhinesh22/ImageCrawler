import scrapy
import re
from ..items import ImagecrawlerItem


class ScrapyTutSpider(scrapy.Spider):
    name = "imagecrawler"
    page_number = 2
    start_urls = [
        'https://www.loopnet.com/for-sale/san-francisco-ca/retail-properties/'
    ]

    def parse(self, response):
        a = []
        pattern = '[^A-Za-z0-9,.$%]'
        items = ImagecrawlerItem()
        containers = response.css("article.placard.tier4")
        for container in containers:
            crawlingpage_add1 = container.css("h4 a::text").extract()
            crawlingpage_add2 = container.css('.subtitle-beta::text').extract()
            crawlingpage_image = container.css('.carousel-inner:nth-child(2) figure meta::attr(content)').extract()
            rows = container.css("header+ .placard-info .data ul")
            for row in rows:
                crawlingpage_details = row.css('li::text').extract()
                details = [re.sub(pattern, " ", i) for i in crawlingpage_details]
                det = [i.strip() for i in details]
            # details = re.sub(pattern, '', crawlingpage_price)
                items["crawlingpage_details"] = det
            items["crawlingpage_address"] = crawlingpage_add1 + crawlingpage_add2
            items["crawlingpage_image"] = crawlingpage_image
            # items["crawlingpage_cap"] = crawlingpage_cap

            yield items

        next_page = "https://www.loopnet.com/for-sale/san-francisco-ca/retail-properties/" + \
                    str(ScrapyTutSpider.page_number) + ""
        if ScrapyTutSpider.page_number <= 2:
            ScrapyTutSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
