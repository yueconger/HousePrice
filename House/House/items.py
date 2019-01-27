# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AreaItem(scrapy.Item):
    # 区域信息
    pass


class XiaoquItem(scrapy.Item):
    # 小区信息
    xiaoqu_name = scrapy.Field()  # 小区名
    xiaoqu_url = scrapy.Field()  # 小区页面链接
    parent_name = scrapy.Field()  # 所属街道
    detailDesc = scrapy.Field()  # 小区地址
    unit_price = scrapy.Field()  # 小区均价
    unit_price_desc = scrapy.Field()  # 均价描述
    build_history = scrapy.Field()  # 建筑历史
    build_type = scrapy.Field()  # 建筑类型
    property_fee = scrapy.Field()  # 物业费
    property_company = scrapy.Field()  # 物业公司
    build_developer = scrapy.Field()  # 开发商
    build_count = scrapy.Field()  # 栋数
    house_total = scrapy.Field()  # 房屋总数
    nearby_store = scrapy.Field()  # 附件门店
