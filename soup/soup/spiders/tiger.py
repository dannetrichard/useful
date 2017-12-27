# -*- coding: utf-8 -*-
import scrapy
from soup.items import TigerItem


class TigerSpider(scrapy.Spider):
    name = 'tiger'
    custom_settings = {
        'ITEM_PIPELINES': {
            'soup.pipelines_tiger.TigerPipeline': 100,
        },
        'LOG_ENABLED': False
    }

    def start_requests(self):
        url = 'http://so.571xz.com/hzgoods.htm'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ids = response.xpath('//div[contains(@class,"navCate")]//a[text()]/@href').re(r'id=(\d*)')
        names = response.xpath('//div[contains(@class,"navCate")]//a[text()]/text()').extract()
        for i in range(0, len(ids)):
            item = TigerItem()
            item['pid_list'] = {'id': ids[i], 'name': names[i]}
            url = 'http://so.571xz.com/hzgoods.htm?webSite=hz&sort=comp&pid=%s' % ids[i]
            request = scrapy.Request(url=url, callback=self.with_pid_parse)
            request.meta['item'] = item
            yield request

    def with_pid_parse(self, response):
        item = response.meta['item']
        ids = response.xpath('//div[contains(@class,"cates")]//a[text()]/@href').re(r'cid=(\d*)')
        names = response.xpath('//div[contains(@class,"cates")]//a[text()]/text()').extract()
        cid_list = []
        for i in range(len(ids)):
            cid_list.append({"id": ids[i], "name": names[i + 1]})
        item['pid_list']['cid_list'] = cid_list

        ids = response.xpath('//div[contains(@class,"markets")]//a[text()]/@href').re(r'mid=(\d*)')
        names = response.xpath('//div[contains(@class,"markets")]//a[text()]/text()').extract()
        mid_list = []
        for j in range(len(ids)):
            mid_list.append({"id": ids[j], "name": names[j + 1]})
        item['pid_list']['mid_list'] = mid_list
        return item
