# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json


class TigerPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='jinjun123', db='soup', charset='utf8')
        self.cursor = self.db.cursor()
        self.pid_list = []
        self.sid_list = [
            {'id': 'comp', 'name': '综合'},
            {'id': 'popular', 'name': '人气'},
            {'id': 'xp', 'name': '新品'}
        ]

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        parameters = {'pid_list': self.pid_list, 'sid_list': self.sid_list}
        paras = json.dumps(parameters)
        sql = "INSERT INTO paras (id,total,selected) VALUES (1,'%s','%s')" \
              "ON DUPLICATE KEY UPDATE total='%s',selected='%s'" % (
                  paras, paras, paras, paras)
        print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        self.db.close()

    def process_item(self, item, spider):
        self.pid_list.append(item['pid_list'])
