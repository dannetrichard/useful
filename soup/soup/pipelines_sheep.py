# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class SheepPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='jinjun123', db='soup', charset='utf8')
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        for key, val in enumerate(item['xz_id']):
            comp = 10000 - ((item['comp'] - 1) * 56 + key)
            sql = "UPDATE items SET comp = %d WHERE xz_id = '%s'" % (comp, val)
            print(sql)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        print(item)
