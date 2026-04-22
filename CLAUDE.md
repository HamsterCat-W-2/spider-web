# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
poetry install                    # Install dependencies
scrapy crawl <spider_name>        # Run a spider directly
scrapy list                       # List all available spiders
celery -A spider_web.celery_app worker --loglevel=info   # Start Celery worker
```

Prerequisites: Redis must be running on localhost:6379 for Celery tasks.

## Architecture

**Tech stack:** Scrapy (crawling) + Celery (task scheduling) + Redis (broker) + Poetry (dependency management).

**Scrapy project structure:**
- `spider_web/settings.py` — Scrapy, Celery, and Redis configuration in one place
- `spider_web/items.py` — `BaseItem` with `url`, `title`, `crawled_at` fields; extend per spider
- `spider_web/pipelines.py` — `JsonPipeline` exports all items to `data/{spider_name}_{timestamp}.json`
- `spider_web/spiders/` — All spider classes go here
- `spider_web/middlewares.py` — Downloader/spider middlewares (currently empty)

**Celery integration:**
- `spider_web/celery_app.py` — Celery app instance, reads broker/backend from Scrapy settings
- `spider_web/tasks.py` — `run_spider(spider_name, **kwargs)` task wraps `CrawlerProcess`

**Output:** Crawled data goes to `data/`, logs to `logs/spider.log`. Both directories are gitignored except `.gitkeep`.

## Conventions

- All spiders inherit from `scrapy.Spider` and live in `spider_web/spiders/`
- New items should extend `BaseItem` from `items.py`
- New pipelines must be registered in `settings.py` → `ITEM_PIPELINES` with priority numbers
- Redis DB 0 = Celery broker, DB 1 = Celery result backend
