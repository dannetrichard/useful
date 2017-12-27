# -*- coding: utf-8 -*-

import scrapy
import json
import pymysql
from soup.items import SheepItem


class SheepSpider(scrapy.Spider):
    name = 'sheep'
    custom_settings = {
        'ITEM_PIPELINES': {
            'soup.pipelines_sheep.SheepPipeline': 800,
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

        total_pages = 50

        for pid in pid_list:
            base_url = 'http://so.571xz.com/hzgoods.htm?webSite=hz&pid=%s&sort=comp&page=' % (pid['id'])
            for i in range(1, total_pages + 1):
                url = base_url + str(i)
                item = SheepItem()
                item['comp'] = i
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['item'] = item
                yield request

    def parse(self, response):
        item = response.meta['item']
        item['xz_id'] = response.xpath('//div[@class="goodsitem"]/a/@href').re(r'id=(\d*)')
        return item
