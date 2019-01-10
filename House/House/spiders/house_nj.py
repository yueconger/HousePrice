# -*- coding: utf-8 -*-
import scrapy


class HouseNjSpider(scrapy.Spider):
    name = 'house_nj'
    allowed_domains = ['lianjia.com']
    url_second_hosuse = 'https://nj.lianjia.com/xiaoqu/'
    local_url = 'https://nj.lianjia.com'
    start_urls = 'https://nj.lianjia.com/xiaoqu/'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'nj.lianjia.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.url_second_hosuse,
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):  # 区
        area_list = response.xpath('//div[@data-role="ershoufang"]/div/a')  
        for area in area_list:
            area_url = ''.join([self.local_url, area.xpath('./@href').extract_first()])
            area_name = area.xpath('./@title')
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=area_url,
                headers=headers,
                callback=self.parse_street
            )

    def parse_street(self, response):  # 街道
        street_list = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')  # 街道按拼音分类
        for street in street_list:
            street_url = ''.join([self.local_url, street.xpath('./@href').extract_first()])
            street_name = street.xpath('./text()').extract_first()
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=street_url,
                headers=headers,
                callback=self.parse_xiaoqu
            )

    def parse_xiaoqu(self, response):  # 街道下所有小区
        xiaoqu_list = response.xpath('//ul[@class="listContent"]/li')
        for xiaoqu in xiaoqu_list:
            detail_xiaoqu_url = xiaoqu.xpath('./a@href').extract_first()  # 小区详情展示页
            detail_xiaoqu_name = xiaoqu.xpath('./a@alt').extract_first()  # 小区名称
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=detail_xiaoqu_url,
                headers=headers,
                callback=self.parse_xiaoqu_info
            )

    def parse_xiaoqu_info(self, response):  # 小区详细信息
        detailDesc = response.xpath('//div[@class="detailDesc"]').extract_first()  # 小区地址
        xiaoquUnitPrice = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').extract_first()  # 小区均价  单位 元/㎡
        xiaoquUnitPriceDesc = response.xpath('//span[@class="xiaoquUnitPriceDesc"]/text()').extract_first()  # 小区均价详情

        xiaoquInfo_list = response.xpath('//div[@class="xiaoquInfo"]/div')
        for xiaoquInfo in xiaoquInfo_list:
            


