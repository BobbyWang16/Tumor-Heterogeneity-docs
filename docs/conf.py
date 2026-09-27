"""Build user documentation without importing imaging dependencies."""
from pathlib import Path
import re

project = "Tumor Heterogeneity"
author = "Tumor Heterogeneity contributors"
copyright = "2026, Tumor Heterogeneity contributors"
release = "0.2.0"
extensions = ["myst_parser"]
source_suffix = {".md": "markdown"}
master_doc = "index"
language = "zh_CN"
html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_theme_options = {"navigation_depth": 3, "collapse_navigation": False}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options.update({"collapse_navigation": True, "style_nav_header_background": "#163b4c"})
html_show_sourcelink = False


def page_language(app, pagename, templatename, context, doctree):
    """Switch between corresponding pages without depending on a hosted URL."""
    english = pagename.startswith("en/")
    counterpart = pagename[3:] if english else "en/" + pagename
    if counterpart not in app.env.found_docs:
        counterpart = "index" if english else "en/index"
    context.update(
        language="en" if english else "zh-CN",
        language_target=counterpart,
        language_label="简体中文" if english else "English",
        language_current="English" if english else "简体中文",
        master_doc="en/index" if english else "index",
        root_doc="en/index" if english else "index",
        docstitle=f"{project} {release}",
        localized_navigation=[
            {"path": ("en/" if english else "") + slug, "title": en if english else zh}
            for slug, zh, en in [
                ("index", "欢迎使用", "Welcome"),
                ("installation", "安装", "Installation"),
                ("concepts", "基本概念", "Basic concepts"),
                ("visual-guide", "可视化图解", "Visual guide"),
                ("getting-started", "快速入门", "Getting Started"),
                ("design-principles", "设计原理", "Design principles"),
                ("data-and-batch", "数据与批处理", "Data and batch processing"),
                ("configuration", "参数配置", "Configuration"),
                ("models", "模型与输出", "Models and outputs"),
                ("api", "API 参考", "API Reference"),
                ("faq", "常见问题", "FAQ"),
                ("package-design", "包发布设计", "Package design"),
                ("contributing", "开发与文档维护", "Contributing"),
            ]
        ],
    )


def setup(app):
    app.connect("html-page-context", page_language)
