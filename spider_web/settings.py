BOT_NAME = "spider_web"

SPIDER_MODULES = ["spider_web.spiders"]
NEWSPIDER_MODULE = "spider_web.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrent requests
CONCURRENT_REQUESTS = 16

# Download delay (seconds)
DOWNLOAD_DELAY = 1

# User-Agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Proxy (set your proxy here for geo-restricted sites)
# HTTP_PROXY = "http://your-proxy:port"
# HTTPS_PROXY = "http://your-proxy:port"

# Default output encoding
FEED_EXPORT_ENCODING = "utf-8"

# Pipelines
ITEM_PIPELINES = {
    "spider_web.pipelines.JsonPipeline": 300,
}

# Log
LOG_LEVEL = "INFO"
LOG_FILE = "logs/spider.log"

# Playwright (for JS-rendered pages)
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Celery / Redis
REDIS_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
