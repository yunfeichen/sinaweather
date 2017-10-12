# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item, Field

from scrapy import Selector, Request

from sinaweather.items import SinaweatherItem


class NgaSpider(scrapy.Spider):
    name = "sinaweatherSpider"
    host = "http://weather.sina.com.cn"
    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "http://weather.sina.com.cn/china/",
    ]

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield Request(url=url, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        selector = Selector(response)
        province_list = selector.xpath("//div[@class='wd_domestic']/div[@class='wd_province']/div/div/div/a[@href]")
        for province in province_list:
            province_name = province.xpath('string(.)').extract_first()
            print province_name
            province_url = province.xpath('@href').extract_first()
            print province_url
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            yield Request(url=province_url, callback=self.parse_city)
            # 可以在此处解析翻页信息，从而实现爬取版区的多个页面
            #exit(0)

    # 帖子的解析函数，解析一个帖子的每一楼的内容
    def parse_city(self, response):
        pro_selector = Selector(response)
        city_list = pro_selector.xpath("//td/a[@href]")
        for city in city_list:
            city_name = city.xpath('string(.)').extract_first()
            print city_name
            city_url = city.xpath('@href').extract_first()
            print city_url
            yield Request(url=city_url, callback=self.parse_dist)

    def parse_dist(self, response):
        selector = Selector(response)
        dist_list = selector.xpath("//div[@id='slider_w']")
        item = SinaweatherItem()
        item['cityurl'] = dist_list.xpath("@data-cityurl").extract()
        item['citytemp'] = dist_list.xpath("@data-citytemp").extract()
        item['citycode'] = dist_list.xpath("@data-citycode").extract()
        item['citycnname'] = dist_list.xpath("@data-citycnname").extract()
        item['cityenname'] = dist_list.xpath("@data-cityenname").extract()
        item['weathercode'] = dist_list.xpath("@data-weathercode").extract()
        item['weathername'] = dist_list.xpath("@data-weathername").extract()
        # print item['cityurl']
        # print item['citytemp']
        # print item['citycnname']
        # print item['cityenname']
        # print item['weathercode']
        # print item['weathername']

        yield item
