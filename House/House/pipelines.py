# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HousePipeline(object):
    def process_item(self, item, spider):
        return item


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

