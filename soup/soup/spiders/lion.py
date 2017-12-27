# -*- coding: utf-8 -*-
import scrapy
import json
from soup.items import LionItem
import pymysql


class LionSpider(scrapy.Spider):
    name = 'lion'
    custom_settings = {
        'ITEM_PIPELINES': {
            'soup.pipelines_pig.PigPipeline': 10,
            'soup.pipelines_lion.BasicPipeline': 100,
            'soup.pipelines_lion.DescriptionPipeline': 200,
            'soup.pipelines_lion.CatePropsPipeline': 300,
            'soup.pipelines_lion.PicturePipeline': 400,
            'soup.pipelines_lion.SkuPropsPipeline': 500,
            'soup.pipelines_lion.CpvMemoPipeline': 600,
            'soup.pipelines_lion.InputCustomCpvPipeline': 700,
            'soup.pipelines_lion.BeePipeline': 800,
        },
        #'LOG_ENABLED': False
    }

    def start_requests(self):
        db = pymysql.connect(host=self.settings['Host'], user=self.settings['USER'], passwd=self.settings['PASSWD'], db=self.settings['DB'], charset=self.settings['CHARSET'])
        cursor = db.cursor()
        sql = 'SELECT * FROM items WHERE mid=601 AND store_name=8307 AND cid=50008900'
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            db.commit()
            print(result)
        except:
            db.rollback()

        for x in result:
            item = LionItem()
            item['pid'] = x[3]
            item['cid'] = x[4]
            item['mid'] = x[5]
            url = 'http://hz.571xz.com/item.htm?id=' + x[6]
            request = scrapy.Request(url=url, callback=self.detail_page)
            request.meta['item'] = item
            yield request

    def detail_page(self, response):
        item = response.meta['item']
        item['num_id'] = response.xpath('//div[@class="goodsTitle"]//a/@href').re_first(r'id=(\d*)')
        item['title'] = response.xpath('//div[@class="goodsTitle"]//a/text()').extract_first()
        item['store_name'] = response.xpath('//div[@class="storeNamebox"]/h3/text()').re_first('([a-zA-Z0-9\-]+)')
        item['xz_id'] = response.url[32:]
        item['picture'] = response.xpath('//div[@class="imageBox"]//a/@href').extract()
        item['description'] = response.xpath('//div[@class="goodsDetail"]//img/@data-original').extract()
        item['cateProps'] = response.xpath('//div[@class="goodsAttribute"]//li/text()').extract()
        item['colorsMeta'] = json.loads(
            response.xpath('//div[@class="leftCol2"]//script/text()').re_first(r'colorsMeta = ([^;]*);'))
        item['sizesMeta'] = json.loads(
            response.xpath('//div[@class="leftCol2"]//script/text()').re_first(r'sizesMeta = ([^;]*);'))
        item['piPrice'] = response.xpath('//div[@class="leftCol2"]//script/text()').re_first(r'piPrice = \'([^\']*)\'')
        item['minPrice'] = response.xpath('//li[@class="minprice"]//em/text()').extract_first()
        if item['minPrice'] is None:
            item['minPrice'] = item['piPrice']
        item['seller_code'] = response.xpath('//div[@class="goodsNumber"]/span[1]/em/text()').extract_first()
        if item['seller_code'] is None:
            item['seller_code'] = ''
        item['list_time'] = response.xpath('//div[@class="goodsNumber"]/span[2]/em/text()').extract_first()
        return item