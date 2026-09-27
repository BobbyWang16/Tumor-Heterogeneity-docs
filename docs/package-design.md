# Python 包发布设计

本页是**待实现方案**，不属于当前 API 承诺。用户指南的示例均使用现有接口。

## 命名与职责

建议保留发行名 `tumor-heterogeneity`，将公开导入名改为 `tumor_heterogeneity`。这样领域含义清晰，也避免与第三方 `ITHscore` 名称混淆。发行名能否用于 PyPI，需在发布前确认。

```text
pyproject.toml
src/
└── tumor_heterogeneity/
    ├── __init__.py
    ├── extractor.py       # 面向用户的统一入口
    ├── config.py          # 参数定义与校验
    ├── io.py              # 影像及空间元数据
    ├── preprocessing.py
    ├── models/            # 七种模型
    ├── pipeline/          # 队列执行
    ├── visualization/
    └── survival/
examples/
tests/
docs/
```

这里的 `src/` 是源码布局目录，不再作为公开 Python 包名。

## 建议的统一入口

以下仅为 API 草案，当前不可运行：

```python
# Proposed API — not implemented
from tumor_heterogeneity import HeterogeneityExtractor

extractor = HeterogeneityExtractor(models=["bih", "dhi"])
result = extractor.execute("image.nii.gz", "mask.nii.gz")
```

统一提取器应承担输入空间校验、预处理、模型配置、错误报告和结果来源记录。底层仍保留各模型的数组接口，便于方法开发。

结果建议统一包含 `scores`、`features`、`maps`、`diagnostics`；地图导出必须携带原点、方向和间距。批量与单病例结果应共享同一结构定义。

## 子项目关系

| 项目 | 发布建议 |
| --- | --- |
| 七模型 ITH | 主包核心 |
| QuanTAV | 保留独立 `quantav-py`，未来通过适配器集成 |
| DualCT | 待输入输出和元数据协议稳定后接入扩展；目前是双期 CT 脚本，不应自动称为双能 CT 支持 |
| 基因与 R 分析 | 研究工作流/示例，不作为主包导入时的依赖 |
| 第三方 ITHscore | 保留独立来源与许可证，避免未经整理直接再发布 |

不要在主包安装时纳入数据、模型结果、R 工作区或嵌套 Git 仓库。

## 发布顺序

1. 统一版本号来源，完成导入名迁移及兼容策略。
2. 修复预处理方向 API，验证掩膜与 CT 的物理空间处理。
3. 清理未生效配置字段，并固定模型结果结构与参数校验。
4. 添加安装后的 CLI 入口，统一路径、日志与错误码。
5. 验证 wheel/sdist 在全新环境中的安装和示例；建立支持版本矩阵。
6. 明确主包许可、第三方归属及引用信息。
7. 接入 Read the Docs，构建版本化文档，再决定 PyPI 发布。

文档网站上线与 PyPI 发布相互独立。`.readthedocs.yaml` 只配置文档构建，不会发布 Python 安装包。
