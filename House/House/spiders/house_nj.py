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

    def parse(self, response):
        area_list = response.xpath('//div[@data-role="ershoufang"]/div/a')  
        for area in area_list:
            area_url = ''.join([self.local_url, area.xpath('./@href').extract_first()])
            area_name = area.xpath('./@title')
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=area_url,
                headers=headers,
                callback=self.parse_xiaoqu_large
            )

    def parse_xiaoqu_large(self, response):
        xiaoqu_list = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')  # 小区按拼音分类
        for xiaoqu in xiaoqu_list:
            xiaoqu_url = ''.join([self.local_url, xiaoqu.xpath('./@href').extract_first()])
            xiaoqu_name = xiaoqu.xpath('./text()').extract_first()
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=xiaoqu_url,
                headers=headers,
                callback=self.parse_xiaoqu_small
            )

    def parse_xiaoqu_small(self, response):
        pass