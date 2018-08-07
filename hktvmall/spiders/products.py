import scrapy
import json
import datetime

def m_get(search, x): ##modified list and dict retriving function. Return None when KeyError or IndexError raise.
    if type(search) == dict:
        return search.get(x, None)
    elif type(search) == list:
        try:
            return search[x]
        except IndexError:
            return None
    else:
        return None

class ProductsScrapper(scrapy.Spider):
    name = 'products'
    api_url = 'https://www.hktvmall.com/hktv/en/ajax/search_products?query=""%3Arelevance&pageSize=1000&currentPage={}'
    start_urls = [api_url.format(0)]

    def parse(self, response):
        data = json.loads(response.text)
        for product in data['products']:
            yield{
            'name': m_get(product,'name'),
            'code': m_get(product,'code'),
            'brand': m_get(product,'brandName'),
            'packing_spec' : m_get(product, 'packingSpec'),
            'price' : m_get(m_get(product,'price'),'value'),
            'promotion_price' : m_get(m_get(product,'promotionPrice'),'value'),
            'category_name' : m_get(m_get(m_get(product,'categories'),0),'name'),
            'category_code' : m_get(m_get(m_get(product,'categories'),0),'code'),
            'store_name' : m_get(m_get(product,'store'),'name'),
            'store_code' : m_get(m_get(product,'store'),'code'),
            'rating' : m_get(product,'averageRating'),
            'stock_status' : m_get(m_get(m_get(product,'stock'),'stockLevelStatus'),'code'),
            'country_of_origin': m_get(product,'countryOfOrigin'),
            'delivery_name': m_get(m_get(product,'deliveryLabel'),'name'),
            'url': m_get(product,'url'),
            'image_url':m_get(m_get(m_get(product,'images'),0),'url'),
            'last_update': datetime.datetime.now()
            }
        current_page = data['pagination']['currentPage']
        n_pages = data['pagination']['numberOfPages'] ## check left pages from JSON itself
        if current_page < n_pages:
            next_page = current_page+1
            print('Progress: {0:.2f}%'.format(current_page/n_pages*100))
            yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)