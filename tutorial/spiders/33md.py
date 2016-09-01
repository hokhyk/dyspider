# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from tutorial.items import *
from datetime import datetime
import re
class A33mdSpider(scrapy.Spider):
    name = "kanxi"
    depth = 0
    allowed_domains = ["kanxi123.com"]
    start_urls = (
        "http://www.kanxi123.com/sort/hd/",
        "http://www.kanxi123.com/sort/1/",
        "http://www.kanxi123.com/sort/2/",
        "http://www.kanxi123.com/sort/3/",
        "http://www.kanxi123.com/sort/4/",
        "http://www.kanxi123.com/sort/5/",
        "http://www.kanxi123.com/sort/6/",
        "http://www.kanxi123.com/sort/7/",
        "http://www.kanxi123.com/sort/27/",
        "http://www.kanxi123.com/sort/28/",
        "http://www.kanxi123.com/sort/29/",
        "http://www.kanxi123.com/sort/30/",
        "http://www.kanxi123.com/sort/31/",
        "http://www.kanxi123.com/sort/32/",
        "http://www.kanxi123.com/sort/33/",
        "http://www.kanxi123.com/sort/34/",
                  )

    def parse(self, response):

        # lasttime = '1900-8-17 4:38:54'
        # lasttime = datetime.strptime(lasttime, '%Y-%m-%d %H:%M:%S')
        # import re
        pa = re.compile(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})')
        for sel in response.css('.k_list-lb'):
            item = TutorialItem()
            item['tags'] = ",".join(sel.css('.k_list-lb-2').xpath('div[4]/a/text()').extract())
            item['title'] = sel.css('.k_list-lb-2').xpath('div[1]/a/text()').extract()[0]
            try:
                item['year'] = sel.css('.k_list-lb-2').xpath('div[2]/a/text()').extract()[0]
            except:
                item['year'] = sel.css('.k_list-lb-2').xpath('div[2]/span/text()').extract()[0]
            #item['actors'] = ",".join(sel.css('.k_list-lb-2').xpath('div[3]/div[1]/a/text()').extract())
            # item['coverlink']=sel.css('#k_upnew-1d-img a img').xpath('@src').extract()[0]
            item['link'] = 'http://www.kanxi123.com' + sel.css('.k_list-lb-2').xpath('div[1]/a[1]/@href').extract()[0]
            try:
                s = sel.css('.k_list-lb-2').xpath('div[7]/text()').extract()[0]
                nowtime = pa.search(s).groups()[0]
                # print(nowtime)
                item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
            except:
                nowtime = str(datetime.now())
                item['datetime'] = datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
            # yield item

            #if item['datetime'] > lasttime:
            res = scrapy.Request(item['link'], self.parse_film_html)
            res.meta['item'] = item
            yield res
        next_page = response.css('div.k_pape a')[-1]
        if next_page.xpath('text()').extract()[0]=='下一页' and self.depth <2:
            self.depth+=1
            url = response.urljoin(next_page.xpath('@href').extract()[0])
            yield scrapy.Request(url, self.parse)

    def parse_film_html(self, response):
        item = response.meta['item']
        item['director']=response.css('.k_jianjie-3a-2b a').xpath('text()').extract()[-1]
        try:
            item['intro']=response.css('#link-report').xpath('text()').extract()[-1]
        except:
            item['intro']=response.css('#link-report span').xpath('text()').extract()[-1]
        item['coverlink']=response.css('#k_jianjie-2b a img').xpath('@src').extract()[0]
        item['actors']=','.join(response.css('.k_jianjie-3a-3b a').xpath('text()').extract())
        item['downloadlink']="\n".join(response.css('.k_jianjie-3a-7a-link a').xpath('@href').extract())+' \n'+"\n".join(response.css('.k_jianjie-3a-7a-pass').xpath('text()').extract())
        item['country']=response.css('.k_jianjie-3a-2b').xpath('text()').extract()[0]
        yield item