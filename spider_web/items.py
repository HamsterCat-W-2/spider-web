import scrapy


class BaseItem(scrapy.Item):
    """Base item with common fields for all spiders."""
    url = scrapy.Field()
    title = scrapy.Field()
    crawled_at = scrapy.Field()
