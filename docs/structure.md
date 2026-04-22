⏺ 整个项目按数据流向可以这样理解：

入口(settings.py) → 爬虫(spiders/dazn.py) → 数据模型(items.py) → 存储(pipelines.py) → 输出(data/\*.json)

逐个模块看：

---

1. pyproject.toml — 项目配置

- Python 3.9+，用 Poetry 管理依赖
- 核心依赖：scrapy（爬虫框架）、scrapy-playwright（JS 渲染）、celery（任务调度）、redis

2. scrapy.cfg — Scrapy 入口配置

- 告诉 Scrapy 去哪里读 settings，就是指向 spider_web/settings.py

3. spider_web/settings.py — 全局配置中心

- SPIDER_MODULES → 告诉 Scrapy 去哪找爬虫（spider_web/spiders/ 目录）
- DOWNLOAD_HANDLERS → 配置 Playwright 处理 HTTP/HTTPS 请求（让 Scrapy 能渲染 JS 页面）
- TWISTED_REACTOR → 异步 reactor，Playwright 必需
- ITEM_PIPELINES → 数据走 JsonPipeline 处理
- ROBOTSTXT_OBEY = True → 遵守 robots.txt
- DOWNLOAD_DELAY = 1 → 每次请求间隔 1 秒，避免被封

4. spider_web/items.py — 数据模型

- BaseItem — 基础字段：url、title、crawled_at
- DaznItem — 继承 BaseItem，加了 image_url、description、section，专门给 DAZN 爬虫用

5. spider_web/spiders/dazn.py — 核心爬虫逻辑  
   整个流程是：
1. start_requests() → 发起请求，配置 Playwright 参数（UA、视口、地区）
1. 页面加载后 → 尝试点掉 cookie 弹窗
1. 滚动页面触发懒加载
1. page.evaluate() 用 JS 在浏览器里遍历 DOM → 按 h2 分区提取图片 + 标题
1. 每条数据构造 DaznItem yield 出去

1. spider_web/pipelines.py — 数据管道

- JsonPipeline：爬虫开始时准备文件，每条 item 存入内存数组，爬虫结束时一次性写成 JSON 到 data/ 目录
- 文件名格式：{spider名}\_{时间戳}.json  


7. spider_web/celery_app.py + tasks.py — 任务调度（当前备用）

- celery_app.py → 连接 Redis，配置序列化和时区
- tasks.py → 定义了 run_spider 任务，可以通过 Celery 远程触发爬虫运行
- 目前先不用，等需要定时任务或分布式调度时启用

---

总结一下，当前核心数据流：

scrapy crawl dazn
→ settings.py 读取配置
→ spiders/dazn.py 用 Playwright 打开页面
→ JS 提取图片+描述 → 构造 DaznItem
→ pipelines.py 的 JsonPipeline 写入 JSON
→ data/dazn_20260422_192303.json (651条数据)

有哪个模块想深入了解的吗？
