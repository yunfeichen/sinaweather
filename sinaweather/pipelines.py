# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import MySQLdb

from sinaweather.items import Item

DEBUG = True

dbuser = 'root'
dbpass = ''
dbname = 'weather'
dbhost = '127.0.0.1'
dbport = '3306'

class MiaoPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        # 清空表：
        # self.cursor.execute("truncate table weather;")
        self.conn.commit()

    def process_item(self, item, spider):
        curTime = datetime.datetime.now()
        try:
            self.cursor.execute("""INSERT INTO sinaweather (cityurl, citytemp, citycode, citycnname, cityenname, weathercode, weathername, updateTime)  
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    item['cityurl'][0].encode('utf-8'),
                                    item['citytemp'][0].encode('utf-8'),
                                    item['citycode'][0].encode('utf-8'),
                                    item['citycnname'][0].encode('utf-8'),
                                    item['cityenname'][0].encode('utf-8'),
                                    item['weathercode'][0].encode('utf-8'),
                                    item['weathername'][0].encode('utf-8'),
                                    curTime,
                                )
                                )

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item