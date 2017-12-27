# -*- coding: utf-8 -*-

import scrapy
import json
import pymysql
from soup.items import BeeItem


class BeeSpider(scrapy.Spider):
    name = 'bee'
    custom_settings = {
        'ITEM_PIPELINES': {
            'soup.pipelines_bee.BeePipeline': 800,
        },
        # 'LOG_ENABLED': False,
        # 'DOWNLOAD_DELAY': 0.5
    }

    def start_requests(self):

        db = pymysql.connect(host=self.settings['Host'], user=self.settings['USER'], passwd=self.settings['PASSWD'],
                             db=self.settings['DB'], charset=self.settings['CHARSET'])
        cursor = db.cursor()
        sql = "SELECT selected FROM paras"
        try:
            cursor.execute(sql)
            load_j = cursor.fetchone()
            db.commit()
        except:
            db.rollback()
        db.close()

        load_dict = json.loads(load_j[0])
        pid_list = load_dict['pid_list']

        # 星座女装 棉衣
        # pid_list = [{'id': '16', 'cid_list': [{'id': '50008900'}], 'mid_list': [{'id': '601'}]}]

        total_pages = 5

        for pid in pid_list:
            for cid in pid['cid_list']:
                for mid in pid['mid_list']:

                    base_url = 'http://so.571xz.com/hzgoods.htm?webSite=hz&mid=%s&pid=%s&cid=%s&sort=xp&page=' % (
                        mid['id'], pid['id'], cid['id'])
                    for i in range(1, total_pages + 1):
                        url = base_url + str(i)
                        item = BeeItem()
                        item['pid'] = pid['id']
                        item['cid'] = cid['id']
                        item['mid'] = mid['id']
                        request = scrapy.Request(url=url, callback=self.parse)
                        request.meta['item'] = item
                        yield request

    def parse(self, response):
        item = response.meta['item']

        item['xz_id'] = response.xpath('//div[@class="goodsitem"]/a/@href').re(r'id=(\d*)')
        item['picture'] = response.xpath('//div[@class="goodsitem"]//img/@data-original').re(r'([ -~]*)_240x240')
        item['title'] = response.xpath('//div[@class="goodsitem"]//p[@class="title"]/a/text()').extract()
        item['price'] = response.xpath(
            '//div[@class="goodsitem"]//p[@class="p1"]/span[@class="pricebox"]/text()').re(r'(\d*)\.')
        item['store_name'] = response.xpath(
            '//div[@class="goodsitem"]//div[@class="p3"]/span[@class="storeName"]/a/@title').re(r' ([A-z\d]*)')
        item['store_id'] = response.xpath(
            '//div[@class="goodsitem"]//div[@class="p3"]/span[@class="storeName"]/a/@href').re(r'id=(\d*)')
        item['seller_nick'] = response.xpath(
            '//div[@class="goodsitem"]//div[@class="p3"]/a[@class="imAliww"]/@href').re(r'touid=([^&]*)&')
        return item
