# pyproject.toml 前端开发者指南

## 一句话理解

`pyproject.toml` 就是 Python 的 **`package.json`**，Poetry 就是 Python 的 **pnpm/yarn**。

## 逐段对照

### `[tool.poetry]` → 对应 `package.json` 的顶层字段

```toml
[tool.poetry]
name = "spider-web"          # ← package.json 的 "name"
version = "0.1.0"            # ← package.json 的 "version"
description = "Web crawler..." # ← package.json 的 "description"
authors = ["guoxuan.wang"]   # ← package.json 的 "author"
readme = "README.md"         # ← 没有对应，声明项目说明文件
packages = [{include = "spider_web"}]  # ← 类似 "main" 字段，告诉打包工具入口包是哪个
```

### `[tool.poetry.dependencies]` → 对应 `package.json` 的 `"dependencies"`

```toml
[tool.poetry.dependencies]
python = "^3.9"              # ← 类似 package.json 的 "engines": {"node": ">=18"}
scrapy = "^2.11"             # ← 类似 "scrapy": "^2.11"，生产依赖
scrapy-playwright = "^0.0.41"
celery = "^5.3"
redis = "^5.0"
```

### `[tool.poetry.group.dev.dependencies]` → 对应 `"devDependencies"`

```toml
[tool.poetry.group.dev.dependencies]
ipython = "^8.0"             # ← 类似 "devDependencies" 里的 eslint、prettier
```

### `[build-system]` → 对应 `package-lock.json` 背后的引擎声明

```toml
[build-system]
requires = ["poetry-core"]            # ← 类似声明用 npm 还是 yarn 来构建
build-backend = "poetry.core.masonry.api"
```

## 常用命令对照表

| Node.js (npm/pnpm) | Python (Poetry) | 作用 |
|---|---|---|
| `npm init` | `poetry init` | 初始化项目 |
| `npm install` | `poetry install` | 安装所有依赖 |
| `npm install axios` | `poetry add scrapy` | 添加生产依赖 |
| `npm install -D jest` | `poetry add --group dev ipython` | 添加开发依赖 |
| `npm run dev` | `poetry run scrapy crawl dazn` | 在虚拟环境中执行命令 |
| `package-lock.json` | `poetry.lock` | 锁定依赖版本 |
| `node_modules/` | `.venv/`（虚拟环境） | 依赖安装位置 |

## 版本号语法对照

| 语法 | npm 含义 | Poetry 含义 | 效果一样吗 |
|---|---|---|---|
| `^2.11` | `>=2.11.0 <3.0.0` | `>=2.11.0 <3.0.0` | 是 |
| `~2.11` | `>=2.11.0 <2.12.0` | `>=2.11.0 <2.12.0` | 是 |
| `*` | 任意版本 | 任意版本 | 是 |

## 关键区别

1. **虚拟环境**：Node.js 用 `node_modules/` 隔离，Python 用 venv（`.venv/`）隔离——整个 Python 解释器 + 依赖都在一个独立目录里
2. **锁文件**：`poetry.lock` 作用等同于 `package-lock.json`/`pnpm-lock.yaml`，保证团队安装相同版本
3. **全局安装**：npm 有 `-g`，Poetry 不推荐全局安装包，所有东西都在项目 venv 里
