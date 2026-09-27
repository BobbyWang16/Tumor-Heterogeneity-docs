# 数据与批处理

## 输入约定

- CT 使用三维、有限数值的 HU 数据，掩膜为同形状、非空的三维前景。
- CT 与掩膜必须事先处于相同空间：尺寸、间距、原点、方向及解剖配准均一致。
- 当前 HAB、PTH、SHI 等实现使用单位体素间距；全模型比较应先统一到 **1 × 1 × 1 mm**。配置字段不等于自动完成重采样。
- PTH 需要肿瘤外围组织，准备输入时不要紧贴肿瘤边界裁剪。
- 各病例使用一致的预处理规则，保存窗宽范围、重采样方式和模型参数。

## 数据目录

```text
data/
└── demo/
    ├── image/                  # 原始 CT
    │   └── case001.nii.gz
    ├── mask/                   # 原始分割
    │   └── case001.nii.gz
    ├── image_process/          # 已预处理 CT
    │   └── case001.nii.gz
    ├── mask_process/           # 已预处理分割
    │   └── case001.nii.gz
    └── clinical.xlsx           # 可选，仅生存分析等需要
```

影像和掩膜推荐使用完全相同的病例文件名；默认后缀是 `.nii.gz`。匹配器也处理 `_ct`、`_mask` 等标记，但这可能合并含这些片段的 ID，批处理前应检查匹配结果。

```python
from src.core import DatasetLoader

loader = DatasetLoader("demo", data_root="./data")
print("Matched cases:", len(loader.pairs))
print(loader.pairs[:3])
```

`image_process/` 与 `mask_process/` 都存在时优先选用，否则 Python 数据配置退回 `image/` 与 `mask/`。目录存在不代表内容完整，未匹配文件不会进入评分。

## Python 批处理

```python
from src.core import DataConfig
from src.pipeline import ModelRunner

config = DataConfig(dataset="demo", data_root="./data", output_root="./results")
paths = ModelRunner(config, models=["bih", "dhi"]).run(visualize=False)
print(paths)
```

输出路径：

```text
results/demo/
├── bih/bih_demo.csv
└── dhi/dhi_demo.csv
```

`models=None` 表示所有模型，显式 `models=[]` 不执行模型。CSV 保留病例级分数、特征和标量详情，不保存三维图。异常病例会记录 `error`；无病例或整批无有限分数时抛出异常。

## 命令行

以下是仓库脚本，需要在仓库根目录运行；目前没有安装后的 `ith` 控制台命令。

```bash
python run_all_scores.py --dataset demo --models bih dhi --no-visualize
python run_all_scores.py --dataset demo --models bih dhi --visualize
```

CLI 默认检查预处理目录。`--skip-preprocess-check` 只跳过检查，不会执行预处理或确认输入几何信息。默认的可视化设置来自脚本 `CONFIG`，可用 `--no-visualize` 显式关闭。

仓库还提供 `scripts/preprocess_all.py`；当前预处理函数含 SimpleITK 方向 API 的兼容性问题，详见 [FAQ](faq.md)。首次使用建议先提供已验证的 1 mm 数据，不能把检查目录存在视为预处理成功。

## 生存分析

`clinical.xlsx` 需要 `PatientID` 或 `case_id`、`time`、`event`。时间单位在整个队列中应一致，事件采用 0/1 编码，病例 ID 与影像文件名对应。

```bash
python -m pip install -e ".[survival]"
python run_all_scores.py --dataset demo --models bih dhi --no-visualize --survival
```

当前报告按病例 ID 连接，拟合单变量 Cox，并用中位数划分 KM 组。它不是多变量模型训练、独立验证或自动临床风险分层流程。
