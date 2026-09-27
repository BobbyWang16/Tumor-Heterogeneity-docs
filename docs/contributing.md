# 开发与文档维护

本网站从独立公开文档仓库 `BobbyWang16/Tumor-Heterogeneity-docs` 构建。该仓库只包含文档；下方算法测试命令需要访问私有实现仓库，并在其根目录运行。文档构建命令可以直接在公开文档仓库运行。

## 本地测试

```bash
python -m pip install -e ".[dev,survival,analysis]" -e ./QuanTAV
python -m pytest
python examples/quickstart.py
python QuanTAV/smoke_test.py
```

完整测试包含 QuanTAV 与可选分析依赖，因此仅安装核心包不足以执行所有测试。

## 构建文档

文档使用 Sphinx、MyST Markdown 和 Read the Docs 主题：

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

打开 `docs/_build/html/index.html` 即可浏览。构建不导入影像算法，也不依赖研究数据。Read the Docs 配置只安装文档依赖。

## 双语维护

中文源文件位于 `docs/`，英文对应页位于 `docs/en/`。一次构建同时生成两种语言；每页的语言链接指向对应章节，而不是返回首页。英文入口是 `docs/_build/html/en/index.html`。

当前采用一个双语站点，不需要分别维护两个 Read the Docs 翻译项目。搜索涵盖两种语言。新增或修改面向用户的页面时，应同步维护中英文，保持代码标识与示例一致。

## 内容维护原则

- README 保持简短：用途、安装、最小示例和文档入口。
- Getting Started 的首个示例应无需下载外部数据即可运行。
- 新功能必须先有实现，再进入用户指南；接口草案留在包设计页。
- 修改特征时同时说明数值定义、单位、输入假设和边界情况。
- 不把未运行的检查、未上线的网站或未发布的软件写成已完成。

已完成的重构范围保留在私有实现仓库根目录 `重构说明.md`；它属于维护记录，不是入门教程。
