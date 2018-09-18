# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy_usage.itemloaders import WechatLoader
from scrapy_usage.items import WechatItem


logger = logging.getLogger('mydomain')


class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['weixin.sogou.com']
    # start_urls = ['http://weixin.sogou.com/weixin?type=1&query=mimeng7']  # 有start_requests的时候可以不用
    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def __init__(self, weibo_id=None, *args, **kwargs):
        super(MydomainSpider, self).__init__(*args, **kwargs)
        self.start_urls = [r'http://weixin.sogou.com/weixin?type=1&query={}'.format(weibo_id)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse)

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        print(response.request.meta)
        wechat_account_list = response.xpath("//ul[@class='news-list2']/li")
        first_weibo_id = wechat_account_list.xpath(".//p[@class='info']/label/text()").extract_first()
        print(first_weibo_id)
        for wechat_account_item in wechat_account_list:
            item_loader = WechatLoader(item=WechatItem(), selector=wechat_account_item)
            item_loader.add_xpath('wechat_id', ".//p[@class='info']/label/text()")
            item_loader.add_xpath('article_url', "./dl[re:test(./dt, '[\u4e00-\u9fa5]{2}文章')]//@href")
            item_loader.add_xpath('verified_info', "./dl[contains(./dt, '认证')]/dd/text()")
            item_loader.add_value('verified_type', wechat_account_item.xpath("./dl/dt/script").re('-?[1-9]\d*'))
            item_loader.add_xpath('description', "./dl[starts-with(./dt, '功能介绍')]/dd/text()")
            item_loader.add_xpath('image_urls', ".//div[@class='img-box']//img/@src")
            item_loader.add_value('file_urls', ['http://v3-dy-y.ixigua.com/cb60a680031cabaa0c9c3f59abb6a41e/5ba06869/video/m/220c22c12774be948cba19e1d18af1ead071159c7770000c5115506a9d5/', 'http://v3-dy-y.ixigua.com/f16919cab4ed8053c33695bd83ae26f5/5ba06844/video/m/220396840062768442e9aee9f6a89f4aa851159f13500002d87e9b5828d/'])
            yield item_loader.load_item()


        #print(response.body)
        logger.info('123')
