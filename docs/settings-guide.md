# settings.py 前端开发者指南

## 一句话理解

`settings.py` 就是 Python 版的 **`.env` + `next.config.js` + `vite.config.ts` 合体**——所有项目配置都集中在这里。

## 逐段讲解

### 1. 项目身份

```python
BOT_NAME = "spider_web"                        # 项目名，日志里会显示
SPIDER_MODULES = ["spider_web.spiders"]         # 爬虫代码目录，类似 pages/ 或 src/routes/
NEWSPIDER_MODULE = "spider_web.spiders"         # 新建爬虫时放哪个目录
```

**前端类比**：相当于 `next.config.js` 里的 `pageExtensions` 或 Nuxt 的 `dir.pages`——告诉框架去哪个目录找页面/组件。

---

### 2. 爬取规则

```python
ROBOTSTXT_OBEY = True       # 遵守网站的 robots.txt
CONCURRENT_REQUESTS = 16     # 同时发 16 个请求
DOWNLOAD_DELAY = 1           # 每次请求间隔 1 秒
USER_AGENT = "Mozilla/5.0..."  # 伪装成浏览器
```

**前端类比**：

| 配置 | 类比 | 说明 |
|---|---|---|
| `ROBOTSTXT_OBEY` | 无直接对应 | 类似尊重 `robots.txt` 的 SEO 规则，True = 守规矩的爬虫 |
| `CONCURRENT_REQUESTS` | 浏览器并发限制（6个） | 同时发多少请求，16 是合理值 |
| `DOWNLOAD_DELAY` | `debounce` / `throttle` | 请求限速，防止被服务器封 IP |
| `USER_AGENT` | HTTP 请求的 `User-Agent` 头 | 伪装身份，让目标网站以为你是普通浏览器 |

---

### 3. 代理配置（当前注释掉）

```python
# HTTP_PROXY = "http://your-proxy:port"
# HTTPS_PROXY = "http://your-proxy:port"
```

**前端类比**：就像在 `axios` 里配 `proxy`，或者在 webpack-dev-server 里配 `proxy`。有些网站有地区限制（比如 DAZN），需要通过代理访问。

---

### 4. 数据管道

```python
ITEM_PIPELINES = {
    "spider_web.pipelines.JsonPipeline": 300,
}
```

**前端类比**：这就像 **Express 的中间件** 或 **Redux 的 middleware**。

- 爬虫 yield 出来的每一条数据（Item），都会经过这里注册的管道依次处理
- 数字 **300** 是优先级（0-1000），数字越小越先执行，类似 Express 中间件的注册顺序
- 当前只注册了一个 `JsonPipeline`，负责把数据写成 JSON 文件
- 以后可以加更多管道，比如下载图片、写入数据库等

```
数据流向：Spider yield Item → JsonPipeline(300) → 写入 data/*.json
```

---

### 5. Playwright 渲染配置（核心）

```python
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
```

**前端类比**：

- `DOWNLOAD_HANDLERS`：默认 Scrapy 用纯 HTTP 请求（类似 `fetch`），只能拿到服务端返回的原始 HTML。换成 Playwright handler 后，相当于**用无头浏览器去打开页面**，等 JS 执行完再拿 DOM——就像你在 `jest` 里用 `jsdom` 或 `playwright` 渲染页面一样
- `TWISTED_REACTOR`：Python 的异步引擎切换。Scrapy 底层用 Twisted（一个老牌异步框架），Playwright 需要 asyncio，这行代码让两者兼容。**前端不用操心这个，Node.js 天生异步，Python 需要显式选择异步引擎**

简单理解：

```
默认 Scrapy：fetch(url) → 拿到原始 HTML（JS 没执行）
加了 Playwright：puppeteer.goto(url) → 等页面渲染完 → 拿到完整 DOM
```

---

### 6. Celery / Redis（任务调度，当前备用）

```python
REDIS_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
```

**前端类比**：相当于 BullMQ + Redis 的任务队列。

- 类似你在 Node.js 里用 `bull` 或 `bullmq` 做后台任务
- `CELERY_BROKER_URL` = Redis 用来传递任务的队列（DB 0）
- `CELERY_RESULT_BACKEND` = Redis 用来存储任务结果（DB 1）
- 目前先配好，等需要定时爬取或分布式调度时再启用

---

## 总结对照表

| settings.py | 前端类比 |
|---|---|
| `SPIDER_MODULES` | Next.js 的 `pageExtensions` |
| `CONCURRENT_REQUESTS` | 浏览器并发限制 |
| `DOWNLOAD_DELAY` | `lodash.throttle` |
| `USER_AGENT` | HTTP 请求头 |
| `ITEM_PIPELINES` | Express/Redux 中间件 |
| `DOWNLOAD_HANDLERS` | fetch → puppeteer 切换 |
| `TWISTED_REACTOR` | 不需要关心（Node.js 天生异步） |
| `CELERY_BROKER_URL` | BullMQ 的 Redis 连接 |
