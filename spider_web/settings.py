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
USER_AGENT = "spider-web (+https://github.com/yourname/spider-web)"

# Default output encoding
FEED_EXPORT_ENCODING = "utf-8"

# Pipelines
ITEM_PIPELINES = {
    "spider_web.pipelines.JsonPipeline": 300,
}

# Log
LOG_LEVEL = "INFO"
LOG_FILE = "logs/spider.log"

# Celery / Redis
REDIS_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
