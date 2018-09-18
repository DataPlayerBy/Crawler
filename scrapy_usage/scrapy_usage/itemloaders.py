from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join, Identity


def remove_seperator_from_string(string):
    yield string.replace('\r', '').replace('\n', '').replace('\t', ' ')


class WechatLoader(ItemLoader):
    default_output_processor = TakeFirst()
    wechat_id_in = MapCompose(str.upper)
    verified_type_in = MapCompose(int)
    description_in = MapCompose(remove_seperator_from_string)
    image_urls_in = MapCompose(lambda image_url: 'http:{}'.format(image_url))
    image_urls_out = Identity()
    file_urls_out = Identity()
