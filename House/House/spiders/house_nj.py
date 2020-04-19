# -*- coding: utf-8 -*-
import scrapy

from House.items import XiaoquItem, SecondHouseItem, ChengJiao


class HouseNjSpider(scrapy.Spider):
    name = 'house_nj'
    allowed_domains = ['lianjia.com']
    url_second_hosuse = 'https://nj.lianjia.com/xiaoqu/?from=rec'
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
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/?from=rec'
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
                meta={'street_name':street_name},
                callback=self.parse_xiaoqu
            )

    def parse_xiaoqu(self, response):  # 街道下所有小区
        street_name = response.meta['street_name']
        print('当前街道:', street_name)
        xiaoqu_list = response.xpath('//ul[@class="listContent"]/li')
        for xiaoqu in xiaoqu_list:
            detail_xiaoqu_url = xiaoqu.xpath('./a/@href').extract_first()  # 小区详情展示页
            print(detail_xiaoqu_url)
            detail_xiaoqu_name = xiaoqu.xpath('./a/img/@alt').extract_first()  # 小区名称
            print('detail_xiaoqu_name', detail_xiaoqu_name)
            headers = self.headers
            headers['Referer'] = 'https://nj.lianjia.com/xiaoqu/'
            yield scrapy.Request(
                url=detail_xiaoqu_url,
                headers=headers,
                meta={'detail_xiaoqu_name': detail_xiaoqu_name, 'detail_xiaoqu_url':detail_xiaoqu_url, 'street_name':street_name},
                callback=self.parse_xiaoqu_info
            )

    def parse_xiaoqu_info(self, response):  # 小区详细信息
        print('-----------')
        item = XiaoquItem()
        street_name = response.meta['street_name']
        xiaoqu_name = response.meta['detail_xiaoqu_name']
        xiaoqu_url = response.meta['detail_xiaoqu_url']
        detailDesc = response.xpath('//div[@class="detailDesc"]/text()').extract_first()  # 小区地址
        xiaoquUnitPrice = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').extract_first()  # 小区均价  单位 元/㎡
        if xiaoquUnitPrice is None:
            xiaoquUnitPrice = ''
        print('xiaoquUnitPrice',xiaoquUnitPrice)
        xiaoquUnitPriceDesc = response.xpath('//span[@class="xiaoquUnitPriceDesc"]/text()').extract_first()  # 小区均价详情
        if xiaoquUnitPriceDesc is None:
            xiaoquUnitPriceDesc = ''
        item['xiaoqu_name'] = xiaoqu_name
        item['xiaoqu_url'] = xiaoqu_url
        item['parent_name'] = street_name
        item['detailDesc'] = detailDesc
        item['unit_price'] = xiaoquUnitPrice
        item['unit_price_desc'] = xiaoquUnitPriceDesc
        xiaoquInfo_list = response.xpath('//div[@class="xiaoquInfo"]/div')
        print('xiaoquInfo_list', xiaoquInfo_list)
        xiaoquInfo_dict = {'建筑年代': 'build_history', '建筑类型': 'build_type', '物业费用': 'property_fee', '物业公司': 'property_company', '开发商': 'build_developer', '楼栋总数': 'build_count', '房屋总数': 'house_total', '附近门店': 'nearby_store'}
        for xiaoquInfo in xiaoquInfo_list:
            xiaoquInfoLabel = xiaoquInfo.xpath('./span[@class="xiaoquInfoLabel"]/text()').extract_first()
            print('xiaoquInfoLabel', xiaoquInfoLabel)
            xiaoquInfoContent = xiaoquInfo.xpath('./span[@class="xiaoquInfoContent"]/text()').extract_first()
            if xiaoquInfoLabel in xiaoquInfo_dict.keys():
                item_key = xiaoquInfo_dict[xiaoquInfoLabel]
                print(item_key)
                item[item_key] = xiaoquInfoContent
        # xiaoqu_info_path = r'E:\SpiderUtils\xiaoqu\xiaoqu.txt'
        # print('item', item)
        # with open(xiaoqu_info_path, 'a+', encoding='utf-8')as f:
        #     f.write(str(item)+',')
        yield item

        house_second_url = response.xpath('//div[@class="goodSellHeader clear"]//a/@href').extract_first()  # 当前地区在售二手房
        house_second_url = response.urljoin(house_second_url)
        chengjiao_url = response.xpath('//div[@class="frameDeal"]/a/@href').extract_first()
        for url in [house_second_url, chengjiao_url]:
            yield scrapy.Request(url=url, callback=self.second_chengjiao, meta={'xiaoqu_name': xiaoqu_name})

    def second_chengjiao(self, response):
        xiaoqu_name = response.meta['xiaoqu_name']
        url = response.url
        if 'chengjiao' in url:
            li_list = response.xpath('//ul[@class="listContent"]/li')
        else:
            li_list = response.xpath('//ul[@class="sellListContent"]/li')
        for li in li_list:
            info_name = li_list.xpath('.//div[@class="title"]/a/text()').extract_first()
            info_href = li_list.xpath('.//div[@class="title"]/a/@href').extract_first()
            yield scrapy.Request(info_href, callback=self.house_info, meta={'xiaoqu_name': xiaoqu_name, 'info_name': info_name, 'info_href': info_href})

    def house_info(self, response):
        """
        二手房信息
        :param response:
        :return:
        """
        second_house_item = SecondHouseItem()
        xiaoqu_name = response.meta['xiaoqu_name']
        info_href = response.meta['info_href']
        info_name = response.meta['info_name']

    def chengjiao_info(self, response):
        """
        成交数据
        :param response:
        :return:
        """
        chengjiao_item = ChengJiao()
        xiaoqu_name = response.meta['xiaoqu_name']
        info_href = response.meta['info_href']
        info_name = response.meta['info_name']
