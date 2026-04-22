from spider_web.celery_app import app
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


@app.task(bind=True)
def run_spider(self, spider_name: str, **spider_kwargs):
    """Run a Scrapy spider as a Celery task."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(spider_name, **spider_kwargs)
    process.start()
