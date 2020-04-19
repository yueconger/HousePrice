# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
import pymysql
from scrapy.pipelines.images import ImagesPipeline

from House.items import ImageItem


class HousePipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 此方法在发送下载请求前调用(此方法本身就是求发送下载请求的)
        if isinstance(item, ImageItem):
            for imgage_url in item['character_img']:
                yield scrapy.Request(url=imgage_url, meta={'item': item})

            # request_objs = super().get_media_requests(item, info)
            #
            # for request_obj in request_objs:
            #     request_obj.item = item
            # return request_objs

    def file_path(self, request, response=None, info=None):
        # 此方法是在图片将要被存储时被调用,获取图片存储路径
        item = request.meta['item']

        # path = super().file_path(request, response, info)
        # img_path = request.item.get('img_path')
        img_path = item['img_path']
        images_store = IMAGES_STORE
        name_path = os.path.join(images_store, img_path)
        image_path = name_path + '.jpg'
        return image_path

class MySQLPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',  # user
            passwd='mysql',  # pass
            db='houseprice',  # db
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        sql = 'insert into xiaoqu(xiaoqu_name,xiaoqu_url,parent_name,detail_desc,unit_price,unit_price_desc,build_history,build_type,property_fee,property_company,build_developer,build_count,house_total,nearby_store) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        lis = (item['xiaoqu_name'], item['xiaoqu_url'], item['parent_name'], item['detailDesc'], item['unit_price'], item['unit_price_desc'], item['build_history'], item['build_type'], item['property_fee'], item['property_company'], item['build_developer'], item['build_count'], item['house_total'], item['nearby_store'])
        print(lis)
        print('数据开始写入')
        self.cur.execute(sql, lis)
        self.client.commit()
        return item

