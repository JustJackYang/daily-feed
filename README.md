# 个人每日信息收集汇总系统

这是一个简单、高效的个人信息聚合系统，帮你自动收集关注的博客、新闻和公众号内容，生成一个每日汇总页面。

## 功能特点

- **多源聚合**：支持 RSS、Atom 等多种 Feed 格式。
- **自定义配置**：通过 `config.json` 轻松管理订阅源。
- **美观展示**：简洁的响应式 HTML 页面，适配电脑和手机。
- **自动更新**：包含 GitHub Actions 配置，支持每天自动抓取并更新页面。

## 快速开始

### 1. 本地运行

1.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```

2.  **配置订阅源**：
    修改 `config.json` 文件，添加你关注的 RSS 链接。
    ```json
    {
      "feeds": [
        { "name": "TechCrunch", "url": "https://feeds.feedburner.com/TechCrunch/" },
        { "name": "我的博客", "url": "https://example.com/feed" }
      ]
    }
    ```

3.  **生成页面**：
    ```bash
    python main.py
    ```
    运行后会生成 `index.html`，直接在浏览器打开即可。

### 2. 自动化部署 (GitHub Actions)

1.  将本项目推送到 GitHub。
2.  在仓库设置中启用 GitHub Pages (Source 选择 `main` 分支或 `gh-pages`)。
3.  GitHub Actions 会每天自动运行 `main.py` 并更新 `index.html`。

## 如何获取 RSS 链接？

- **博客/网站**：通常在网址后加 `/feed` 或 `/rss`。
- **微信公众号**：使用 [WeRSS](https://github.com/cnsilvan/WeRSS) 或 [RSSHub](https://docs.rsshub.app/) 生成。
- **Twitter/X**：使用 [RSSHub](https://docs.rsshub.app/) 生成。

## 目录结构

- `main.py`: 核心脚本，负责抓取和生成页面。
- `config.json`: 配置文件。
- `templates/`: 存放 HTML 模板。
- `.github/workflows/`: GitHub Actions 自动配置。

## 许可证

MIT
