# -*- coding: utf-8 -*-
import scrapy
from IAEA.items import IaeaItem

class IaeaSpiderSpider(scrapy.Spider):
    name = 'IAEA_spider'
    allowed_domains = ['iaea.org']
    start_urls = ['https://www.iaea.org/news']

    def parse(self, response):
        article_list = response.xpath("//div[@class='container']//div[@class='row']//div[@class='grid']")
        for i_item in article_list:
            iaea_items = IaeaItem()
            iaea_items['title'] = i_item.xpath(".//h4/a/text()").extract_first()
            iaea_items['pub_time'] = i_item.xpath(".//span[@class='dateline-published']/text()").extract_first()
            iaea_items['text_link'] = 'https://www.iaea.org' + i_item.xpath(".//h4/a/@href").extract_first()
            yield iaea_items

        next_link = response.xpath("//div[@class='text-center']//ul/li[@class='next']//a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://www.iaea.org" + next_link, callback=self.parse)