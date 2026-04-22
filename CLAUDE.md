# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
poetry install                    # Install dependencies
poetry run playwright install chromium  # Install Playwright browser (first time only)
scrapy crawl <spider_name>        # Run a spider directly
scrapy list                       # List all available spiders
celery -A spider_web.celery_app worker --loglevel=info   # Start Celery worker
```

Prerequisites: Redis must be running on localhost:6379 for Celery tasks.

## Architecture

**Tech stack:** Scrapy (crawling) + scrapy-playwright (JS rendering) + Celery (task scheduling) + Redis (broker) + Poetry (dependency management).

### Data flow

```
scrapy crawl <spider_name>
  → settings.py          读取全局配置（Playwright、并发、管道等）
  → spiders/<name>.py    用 Playwright 打开页面，JS 提取内容，构造 Item
  → items.py             定义数据字段
  → pipelines.py         JsonPipeline 将数据写入 JSON 文件
  → data/<name>_<timestamp>.json
```

### Module overview

| 文件 | 职责 |
|------|------|
| `scrapy.cfg` | Scrapy 入口，指向 settings.py |
| `spider_web/settings.py` | 全局配置：Playwright 渲染器、并发数、下载延迟、管道注册、Celery/Redis 连接 |
| `spider_web/items.py` | 数据模型：`BaseItem`（通用）、`DaznItem`（DAZN 爬虫专用），定义字段 |
| `spider_web/pipelines.py` | `JsonPipeline`：爬虫运行时收集 items，结束后写 `data/{name}_{timestamp}.json` |
| `spider_web/spiders/` | 所有爬虫类放在这里，每个 spider 处理特定站点 |
| `spider_web/middlewares.py` | 下载器/蜘蛛中间件（待扩展） |
| `spider_web/celery_app.py` | Celery 应用实例，连接 Redis，配置序列化和时区 |
| `spider_web/tasks.py` | `run_spider(spider_name, **kwargs)` 任务，通过 Celery 远程触发爬虫 |

### Key settings in settings.py

- `DOWNLOAD_HANDLERS` → 配置 Playwright 处理 HTTP/HTTPS（支持 JS 渲染页面）
- `TWISTED_REACTOR` → asyncio reactor，Playwright 必需
- `ROBOTSTXT_OBEY = True` → 遵守 robots.txt
- `DOWNLOAD_DELAY = 1` → 每次请求间隔 1 秒，避免被封
- `ITEM_PIPELINES` → 数据处理管道及优先级

### Output

- `data/` → 爬取的 JSON 数据（gitignored except `.gitkeep`）
- `logs/spider.log` → 运行日志（gitignored except `.gitkeep`）

## Conventions

- All spiders inherit from `scrapy.Spider` and live in `spider_web/spiders/`
- New items should extend `BaseItem` from `items.py`
- New pipelines must be registered in `settings.py` → `ITEM_PIPELINES` with priority numbers
- Redis DB 0 = Celery broker, DB 1 = Celery result backend
