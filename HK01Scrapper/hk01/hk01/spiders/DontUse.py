# -*- coding: utf-8 -*-
import scrapy
import datetime
import dateutil.parser


class hk01Spider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = 'hk01'
    time_span = datetime.timedelta(days=1, hours=8) ## Type the timespan, in days
    first_tag = True
    parse_num = 228242 ## Type the latest article ID
    raw_url = 'https://www.hk01.com/%E7%A4%BE%E6%9C%83%E6%96%B0%E8%81%9E/{}'
    start_urls = [raw_url.format(parse_num)]

    def parse(self, response):
        if (response.status == 404) | (response.css('time::attr(datetime)').extract_first() == None):
            self.parse_num = self.parse_num - 1
            yield scrapy.Request(url=self.raw_url.format(self.parse_num), callback=self.parse)
        else:
            item = {
                'id':self.parse_num,
                'Publish Time':response.css('time::attr(datetime)').extract_first(),
                'Category':response.css('div.sc-bwzfXH.jruoDg>span>a::text').extract(),
                'Author':response.css('a.sc-gqjmRU.dhKqyP::text').extract(),
                'Discription':response.css('p.wa4tvz-0.hmJMOX.sc-gqjmRU.jTjJUk::text').extract(),
                'Text':response.css('.u02q31-0.gvqXdj.sc-gqjmRU.gBjLGB::text').extract(),
            }
            yield item
            if self.first_tag:
                self.end_time = dateutil.parser.parse(response.css('time::attr(datetime)').extract_first()) - self.time_span
                self.first_tag = False
            publish_date = dateutil.parser.parse(response.css('time::attr(datetime)').extract_first())

            if publish_date > self.end_time:
                self.parse_num = self.parse_num - 1
                yield scrapy.Request(url=self.raw_url.format(self.parse_num), callback=self.parse)