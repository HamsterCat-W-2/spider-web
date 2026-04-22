# scrapy.cfg 前端开发者指南

## 一句话理解

`scrapy.cfg` 就像前端项目根目录的 **配置入口文件**，相当于 `tsconfig.json` 之于 TypeScript——告诉工具链去哪里找核心配置。

## 文件内容

```ini
[settings]
default = spider_web.settings    # ← 告诉 Scrapy：去 spider_web/settings.py 读全局配置

[deploy]
project = spider-web             # ← 项目名，用于 scrapyd 远程部署（当前未用到）
```

## 对照前端理解

| scrapy.cfg | 前端类比 | 作用 |
|---|---|---|
| `[settings]` → `default` | `tsconfig.json` 的 `"compilerOptions"` | 指向具体的配置文件路径 |
| `[deploy]` → `project` | `package.json` 的 `"name"` | 标识项目，用于部署场景 |

具体来说：
- `default = spider_web.settings` 就像 `tsconfig.json` 里写 `"extends": "./paths/to/config"`，只是一个**指针**
- 真正的配置内容全在 `spider_web/settings.py` 里，这个文件本身只负责"指路"

## 为什么需要它

Scrapy 命令行工具（`scrapy crawl`、`scrapy list` 等）启动时，会从**当前目录向上查找** `scrapy.cfg`，找到后就知道：
1. 项目的 settings 在哪 → 加载配置
2. 爬虫代码在哪 → `settings.py` 里的 `SPIDER_MODULES = ["spider_web.spiders"]`

类比：就像你在项目根目录运行 `npm run dev`，npm 会自动找 `package.json` 一样；你运行 `scrapy crawl dazn`，Scrapy 会自动找 `scrapy.cfg`。

## 当前状态

这个文件初始化后**基本不需要改动**，除非你改了包名（比如 `spider_web` → `src`，那就要改成 `default = src.settings`）。
