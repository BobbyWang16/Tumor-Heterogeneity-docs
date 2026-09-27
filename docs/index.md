# Tumor Heterogeneity

**同一个肿瘤，可以从不止一个角度理解。**

```{raw} html
<div class="ith-hero"><p><strong>给我们一张 CT 和一张肿瘤掩膜。</strong><br>工具集把“里面有多不均匀、区域如何排列、边缘是什么样”转成可检查的数值和空间分区。</p><p>先跑通一个小例子，再分析自己的队列。无需先掌握全部七种算法。</p></div>
```

Tumor Heterogeneity 是面向 CT 肿瘤异质性研究的 Python 工具集。主包提供七种评分模型、统一的单病例计算接口、队列 CSV 导出，以及可选的可视化与生存分析。

你可以先用一个不需要下载数据的示例完成首次计算，再将相同接口应用到自己的影像队列。

- **首次使用**：[安装](installation.md) → [Getting Started](getting-started.md)。
- **先理解再动手**：[基本概念](concepts.md) → [为什么这样设计](design-principles.md)。
- **分析自己的队列**：[数据与批处理](data-and-batch.md)。
- **理解计算结果**：[模型与输出](models.md) → [参数配置](configuration.md)。
- **开发与集成**：[API Reference](api.md) → [包发布设计](package-design.md)。

## 当前提供什么？

| 能力 | 输入 | 输出 |
| --- | --- | --- |
| 单病例 ITH 计算 | CT 数组 + 二值掩膜 | score、特征字典、部分模型的空间图 |
| 队列计算 | 配对 NIfTI 文件 | 每模型一个病例级 CSV |
| 队列诊断 | 模型 CSV | 分布、相关性、质量统计等报告 |
| 生存探索 | 评分 + 临床时间/事件表 | 单变量 Cox、KM 曲线 |
| QuanTAV 扩展 | 肿瘤与血管掩膜 | 血管形态及组织特征，独立安装 |

当前发行配置名为 `tumor-heterogeneity`，Python 导入路径暂为 `src`；源码安装方式已提供。本文档不假设包已发布到 PyPI。DualCT、R 脚本及第三方 ITHscore 的边界见 [包发布设计](package-design.md)。

## 从输入到结果

```{raw} html
<div class="ith-flow" aria-label="处理流程">
<div><strong>01 · 准备</strong><small>CT 提供灰度，掩膜标出分析区域。</small></div>
<div><strong>02 · 对齐</strong><small>核对坐标与分辨率，让病例可比较。</small></div>
<div><strong>03 · 描述</strong><small>选择密度、形状或空间分区模型。</small></div>
<div><strong>04 · 检查</strong><small>查看分数、特征、空间图及失败记录。</small></div>
</div>
```

## 应该从哪个模型开始？

先选 **DHI**：它回答“肿瘤内的灰度变化有多大”，输入简单、结果容易理解。想观察区域排列，再看 **HAB / THI**；关心瘤周组织，选择 **PTH**。完整比较见 [模型选择与输出](models.md)。

英文读者可进入 [English documentation](en/index.md)。每一页右上角都可切换到对应语言；示例与接口名称保持一致。

```{toctree}
:maxdepth: 2
:caption: 用户指南

installation
concepts
getting-started
design-principles
data-and-batch
configuration
models
api
faq
```

```{toctree}
:maxdepth: 1
:caption: 开发与发布

package-design
contributing
```

```{toctree}
:maxdepth: 1
:caption: English documentation

en/index
```

## 文档设计来源

信息架构参考 [PyRadiomics 文档](https://pyradiomics.readthedocs.io/en/latest/) 对安装、使用、配置、特征和 API 的分层组织。这里的功能说明与示例依据本仓库实现编写；不是 PyRadiomics 的接口兼容层。
