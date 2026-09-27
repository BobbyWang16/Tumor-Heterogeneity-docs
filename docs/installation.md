# Installation

> 当前实现仓库为私有仓库。以下源码安装步骤仅适用于已有仓库访问权限的用户；尚未提供公开 PyPI 安装。

## 环境要求

主包声明 Python ≥ 3.9；同时使用 QuanTAV 时需要 Python ≥ 3.10。本地入门示例在 Python 3.11 验证，建议新建 3.11 环境。

## 从源码安装

```bash
git clone https://github.com/BobbyWang16/Tumor-Heterogeneity.git
cd Tumor-Heterogeneity
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS：

```bash
source .venv/bin/activate
```

安装主包：

```bash
python -m pip install -e .
```

`-e` 用于源码开发，修改代码后无需重复安装。暂不提供未经验证的 `pip install tumor-heterogeneity` 或 Conda 渠道安装说明。

## 可选依赖

| 用途 | 在仓库根目录执行 |
| --- | --- |
| Cox 与 Kaplan–Meier | `python -m pip install -e ".[survival]"` |
| 基因富集脚本的网络依赖 | `python -m pip install -e ".[analysis]"` |
| 运行测试 | `python -m pip install -e ".[dev]"` |
| 构建文档 | `python -m pip install -e ".[docs]"` |
| QuanTAV 血管特征 | `python -m pip install -e ./QuanTAV` |

`analysis` 仅补充依赖，不会下载表达数据或安装 R/Bioconductor。

## 验证安装

```bash
python -c "from importlib.metadata import version; from src.models import MODEL_REGISTRY; print(version('tumor-heterogeneity')); print(list(MODEL_REGISTRY))"
```

当前主包版本以安装元数据和 `pyproject.toml` 为准。随后运行 [第一次计算](getting-started.md)。
