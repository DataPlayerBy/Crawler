from scrapy.crawler import CrawlerProcess
from scrapy_usage.spiders.mydomain import MydomainSpider
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())
process.crawl(MydomainSpider, weibo_id='mimeng7')
# process.crawl(MydomainSpider2) # 可以加多个
process.start()
process.stop()

