# -*- coding: utf-8 -*-
import scrapy


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = (
        'http://www.dmoz.org/Computers/programming/Languaes/Python/Books/',
        'http://www.dmoz.org/Computers/programming/Languaes/Python/Resources/',
    )

    def parse(self, response):
        filename=response.url.split("/")[-2]+".html"
        with open(filename,"wb") as f:
            f.write(response.body)
