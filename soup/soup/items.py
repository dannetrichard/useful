# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LionItem(scrapy.Item):
    # define the fields for your item here like:
    xz_id = scrapy.Field()
    num_id = scrapy.Field()
    colorsMeta = scrapy.Field()
    sizesMeta = scrapy.Field()
    piPrice = scrapy.Field()
    minPrice = scrapy.Field()
    pid = scrapy.Field()
    mid = scrapy.Field()
    seller_code = scrapy.Field()
    store_name = scrapy.Field()

    title = scrapy.Field()
    cid = scrapy.Field()
    seller_cids = scrapy.Field()
    location_state = scrapy.Field()
    location_city = scrapy.Field()
    price = scrapy.Field()
    num = scrapy.Field()
    approve_status = scrapy.Field()
    has_showcase = scrapy.Field()
    list_time = scrapy.Field()
    description = scrapy.Field()
    cateProps = scrapy.Field()
    postage_id = scrapy.Field()
    has_discount = scrapy.Field()
    picture = scrapy.Field()
    skuProps = scrapy.Field()
    outer_id = scrapy.Field()
    sub_stock_type = scrapy.Field()
    item_weight = scrapy.Field()
    sell_promise = scrapy.Field()
    subtitle = scrapy.Field()
    cpv_memo = scrapy.Field()
    input_custom_cpv = scrapy.Field()


class SoupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BeeItem(scrapy.Item):
    xz_id = scrapy.Field()
    picture = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    store_name = scrapy.Field()
    store_id = scrapy.Field()
    seller_nick = scrapy.Field()
    pid = scrapy.Field()
    cid = scrapy.Field()
    mid = scrapy.Field()


class TigerItem(scrapy.Item):
    pid_list = scrapy.Field()


class SheepItem(scrapy.Item):
    xz_id = scrapy.Field()
    comp = scrapy.Field()
