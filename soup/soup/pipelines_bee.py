# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class BeePipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='jinjun123', db='soup', charset='utf8')
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        for key, val in enumerate(item['xz_id']):
            sql = "INSERT INTO items (xz_id,picture,title,price,store_name,store_id,seller_nick,pid,cid,mid) VALUES (" \
                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE picture='%s'," \
                  "title='%s',price='%s',store_name='%s',store_id='%s',seller_nick='%s',pid='%s',cid='%s',mid='%s'" % (
                      item['xz_id'][key], item['picture'][key], item['title'][key], item['price'][key],
                      item['store_name'][key], item['store_id'][key],
                      item['seller_nick'][key], item['pid'], item['cid'], item['mid'], item['picture'][key],
                      item['title'][key],
                      item['price'][key], item['store_name'][key], item['store_id'][key], item['seller_nick'][key],
                      item['pid'], item['cid'],
                      item['mid']
                  )
            print(sql)
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        print(item)
