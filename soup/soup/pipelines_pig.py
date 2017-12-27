# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

import json


class PigPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='jinjun123', db='soup', charset='utf8')
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        sql = "UPDATE items SET title = '%s'," \
              "picture = '%s'," \
              "num_id = '%s'," \
              "colorsMeta = '%s'," \
              "sizesMeta = '%s'," \
              "piPrice = '%s'," \
              "minPrice = '%s'," \
              "seller_code = '%s'," \
              "list_time = '%s'," \
              "description = '%s'," \
              "cateProps = '%s' WHERE xz_id = '%s'" % (
                  item['title'],
                  json.dumps(item['picture']),
                  item['num_id'],
                  json.dumps(item['colorsMeta']),
                  json.dumps(item['sizesMeta']),
                  item['piPrice'],
                  item['minPrice'],
                  item['seller_code'],
                  item['list_time'],
                  json.dumps(item['description']),
                  json.dumps(item['cateProps']),
                  item['xz_id']
              )
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        return item
