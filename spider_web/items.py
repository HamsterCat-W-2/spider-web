import scrapy


class BaseItem(scrapy.Item):
    """Base item with common fields for all spiders."""
    url = scrapy.Field()
    title = scrapy.Field()
    crawled_at = scrapy.Field()


class DaznItem(scrapy.Item):
    """Item for DAZN page content."""
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    section = scrapy.Field()
    crawled_at = scrapy.Field()
