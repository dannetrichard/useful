# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
import json
import csv
import hashlib


class BasicPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(host='127.0.0.1', user='root', passwd='jinjun123', db='bee', charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        dict = {'50008900': '1340125112', '50013194': '1340125113', '50008898': '1294330315', '162103': '1255457751',
                '50008901': '1294330316', }
        try:
            item['seller_cids'] = dict[item['cid']]
        except:
            item['seller_cids'] = ''
        item['location_state'] = '浙江'
        item['location_city'] = '杭州'
        item['price'] = item['piPrice']
        item['num'] = len(item['colorsMeta']) * len(item['sizesMeta']) * 888
        item['approve_status'] = 1
        item['has_showcase'] = 1
        item['postage_id'] = '10149716421'
        item['has_discount'] = 1
        item['outer_id'] = '%s-%s-P%s-L%s' % (
            item['store_name'], item['seller_code'], item['piPrice'], item['minPrice'])
        item['sub_stock_type'] = 2
        item['item_weight'] = 1
        item['sell_promise'] = 1
        item['subtitle'] = ''

        '''
        获取color的value值
        '''
        text_list = []
        custom = 1
        result = None
        for key, val in enumerate(item['colorsMeta']):
            text = val['text'].split(' ')
            try:
                item['colorsMeta'][key]['memo'] = text[1]
            except:
                pass
            if text[0] not in text_list:
                sql = "SELECT key_id,value FROM props WHERE cid = '%s' AND text = '%s'" % (
                    item['cid'], text[0])
                try:
                    self.cursor.execute(sql)
                    result = self.cursor.fetchone()
                    self.db.commit()
                except:
                    result = None
                    self.db.rollback()
            else:
                result = None
            if result is not None:
                item['colorsMeta'][key]['key_id'] = result[0]
                item['colorsMeta'][key]['value'] = result[1]
                text_list.append(text[0])
            else:
                item['colorsMeta'][key]['key_id'] = '1627207'
                item['colorsMeta'][key]['value'] = str(-1000 - custom)
                custom = custom + 1
        '''
        获取size的value值
        '''
        result = None
        for k, v in enumerate(item['sizesMeta']):
            sql = "SELECT key_id,value FROM props WHERE cid = '%s' AND text = '%s'" % (
                item['cid'], v)
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                self.db.commit()
                if result is not None:
                    item['sizesMeta'][k] = {'key_id': result[0], 'value': result[1], 'text': v}
            except:
                self.db.rollback()

        '''
        获取prop的value值
        '''
        result = None
        for key, val in enumerate(item['cateProps']):
            [key_label, text] = val.split('：')
            if key_label == '品牌':
                item['cateProps'][key] = {'key_id': '20000', 'key_label': '品牌', 'value': '29534', 'text': '其他'}
            else:
                sql = "SELECT key_id,value FROM props WHERE cid = '%s' AND key_label = '%s' AND text = '%s'" % (
                    item['cid'], key_label, text)
                try:
                    self.cursor.execute(sql)
                    result = self.cursor.fetchone()
                    if result is not None:
                        item['cateProps'][key] = {'key_id': result[0], 'key_label': key_label, 'value': result[1],
                                                  'text': text}
                    self.db.commit()
                except:
                    self.db.rollback()

        return item


class DescriptionPipeline(object):
    def process_item(self, item, spider):
        description = ''
        m = hashlib.md5()
        for key, val in enumerate(item['description']):
            # md5 = hashlib.md5()
            # md5.update(str(key).encode(encoding='utf-8'))

            description = description + '<IMG src="FILE:///G:\csv\description\%s-%s-%s\%d.%s" align=middle>' % (
                item['store_name'], item['seller_code'], item['xz_id'], key, val.split('.').pop())
        item['description'] = description
        return item


class CatePropsPipeline(object):
    def process_item(self, item, spider):
        cate_props = ''
        for prop in item['cateProps']:
            try:
                cate_props = cate_props + '%s:%s;' % (prop['key_id'], prop['value'])
            except:
                pass

        for prop in item['colorsMeta']:
            try:
                cate_props = cate_props + '%s:%s;' % (prop['key_id'], prop['value'])
            except:
                pass

        for prop in item['sizesMeta']:
            try:
                cate_props = cate_props + '%s:%s;' % (prop['key_id'], prop['value'])
            except:
                pass
        item['cateProps'] = cate_props
        return item


class PicturePipeline(object):
    def process_item(self, item, spider):
        picture = ''
        for key, val in enumerate(item['picture']):
            picture_name = '%s-%d' % (item['xz_id'], key)
            md5 = hashlib.md5()
            md5.update(picture_name.encode(encoding='utf-8'))
            picture = picture + '%s:%d:%d:|%s;' % (md5.hexdigest(), 1, key, val)
        item['picture'] = picture
        return item


class SkuPropsPipeline(object):
    def process_item(self, item, spider):

        sku_props = ''
        for color in item['colorsMeta']:
            for size in item['sizesMeta']:
                sku_props = sku_props + '%d:%s::%s:%s;%s:%s;' % (
                    round(float(item['price'])), '888', color['key_id'], color['value'], size['key_id'], size['value'])

        item['skuProps'] = sku_props;
        return item


class CpvMemoPipeline(object):
    def process_item(self, item, spider):
        cpv_memo = ''
        for color in item['colorsMeta']:
            try:
                cpv_memo = cpv_memo + '%s:%s:%s;' % (color['key_id'], color['value'], color['memo'])
            except:
                pass
        for size in item['sizesMeta']:
            try:
                cpv_memo = cpv_memo + '%s:%s:%s;' % (size['key_id'], size['value'], size['memo'])
            except:
                pass
        item['cpv_memo'] = cpv_memo
        return item


class InputCustomCpvPipeline(object):
    def process_item(self, item, spider):
        input_custom_cpv = ''
        for color in item['colorsMeta']:
            if int(color['value']) < 0:
                input_custom_cpv = input_custom_cpv + '%s:%s:%s;' % (color['key_id'], color['value'], color['text'])
        item['input_custom_cpv'] = input_custom_cpv
        return item


class BeePipeline(object):
    def open_spider(self, spider):
        self.header = ['title',
                       'cid',
                       'seller_cids',
                       'location_state',
                       'location_city',
                       'price',
                       'num',
                       'approve_status',
                       'has_showcase',
                       'list_time',
                       'description',
                       'cateProps',
                       'postage_id',
                       'has_discount',
                       'picture',
                       'skuProps',
                       'outer_id',
                       'sub_stock_type',
                       'item_weight',
                       'sell_promise',
                       'subtitle',
                       'cpv_memo',
                       'input_custom_cpv']
        with open('G:\\csv\\full.csv', 'w', encoding='utf_16_le') as csvfile:
            csvfile.write('\ufeff')
            version_writer = csv.writer(csvfile, lineterminator="\n", delimiter="\t")
            version_writer.writerow(["version 1.00"])
            writer = csv.DictWriter(csvfile, fieldnames=self.header, lineterminator="\n", delimiter="\t",
                                    quotechar="\"")
            writer.writeheader()
            writer.writeheader()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        dt = dict((key, value) for key, value in item.items() if key in self.header)
        with open('G:\\csv\\full.csv', 'a', encoding='utf_16_le') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.header, lineterminator="\n", delimiter="\t",
                                    quotechar="\"")
            writer.writerow(dt)
