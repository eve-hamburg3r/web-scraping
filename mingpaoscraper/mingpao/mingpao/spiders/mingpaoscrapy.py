import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
import json
import datetime

def clean_tag(html):
    soup = BeautifulSoup(html, 'lxml')
    text = [tag.text for tag in soup.findAll('p') if tag.find('a') == None]
    return ''.join(text)

class MingpaoscrapySpider(scrapy.Spider):
    name = 'mingpaoscrapy'

    def __init__(self, days, *args, **kwargs):
        super(MingpaoscrapySpider, self).__init__(*args, **kwargs)
        self.days = int(days)

    def start_requests(self):
        start_day = datetime.datetime.now() - datetime.timedelta(1)
        for day in range(self.days):
            scrape_day = start_day - datetime.timedelta(day)
            scrape_day = datetime.datetime.strftime(scrape_day,'%Y%m%d')
            print('check:'+scrape_day)
            yield SplashRequest(
                url = 'https://news.mingpao.com/ins/%E6%B8%AF%E8%81%9E/web_tc/section/{}/s00001'.format(scrape_day),
                callback = self.parse_first_news,
            )

    def parse_first_news(self, response):
        first_news_url = response.css('li.list1>a::attr(href)').extract_first()
        yield SplashRequest(
            url = 'https://news.mingpao.com{}'.format(first_news_url),
            callback= self.parse_list
        )

    def parse_list(self, response):
        list_news = response.css('select.txt2>option::attr(value)').extract()
        list_news = [(item.split('/')[-3],item.split('/')[-1]) for item in list_news]
        urls = ['https://news.mingpao.com/dat/ins/ins_web_tc/article1/{}/content_{}.js'.format(item[0], item[1]) for item in list_news]
        for link in urls:
            yield scrapy.Request(url = link, callback=self.parse_news)
    
    def parse_news(self, response):
        data = json.loads(response.text)
        items = {
            'Title':data['TITLE'],
            'Publish date':data['PERIOD']['ATTRIBUTES']['START'],
            'Content':clean_tag(data['DESCRIPTION']),
            'url':response.url
        }
        yield items