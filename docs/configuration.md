# 参数配置

当前通过 Python dataclass 配置模型；尚未实现统一 YAML 参数文件。

## 自定义单病例计算

```python
from dataclasses import asdict
from src.core import DHIConfig
from src.models import DHIModel

config = DHIConfig(clip_percentiles=(1, 99), nbins=32, win_lcv=5)
model = DHIModel(config)
print(asdict(config))
# image、mask 准备好后：result = model.compute(image, mask)
```

## 常用参数

| 模型 | 配置类 | 已接入计算的常用字段 | 默认值 |
| --- | --- | --- | --- |
| DHI | `DHIConfig` | `clip_percentiles`, `nbins`, `win_lcv` | `(1, 99)`, `64`, `3` |
| HAB | `HABConfig` | `k_habitat`, `hu_min`, `hu_max` | `4`, `-1000`, `400` |
| PTH | `PTHConfig` | `ring_mm`, `target_block_size_mm3`, `compactness` | `5.0`, `5000`, `15.0` |
| SHI | `SHIConfig` | `scales` | `[1, 2, 4, 8, 16]` |
| THI | `THIConfig` | `k`, `padding`, `clip`, `n_workers` | `3`, `2`, `(1, 99)`, `4` |
| ITH-FS | `ITHFusionConfig` | `n_clusters`, `scales`, `n_neighbors` | `6`, `[1, 2, 3]`, `20` |

配置文件还声明了一些当前未参与相应计算的字段，例如 `BIHConfig.box_sizes`、`SHIConfig.target_spacing`、`ITHFusionConfig.adaptive_k/use_hog`。不要据此推断它们已控制算法行为。`save_intermediates` 也不代表批处理会自动保存空间图。

## 自定义参数批处理

`ModelRunner` 目前为每个模型创建默认配置。需要自定义参数时，直接使用模型实例：

```python
from src.core import DataConfig, DHIConfig
from src.models import DHIModel

data = DataConfig(dataset="demo", data_root="./data", output_root="./results")
model = DHIModel(DHIConfig(nbins=32, win_lcv=5))
csv_path = model.run_and_save(data)
```

同一输出位置再次运行会覆盖同名 CSV。参数对照实验应使用不同的 `output_root` 或 `csv_name`。

## 保存实验配置

```python
import json
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from src.core import DHIConfig

record = {
    "package_version": version("tumor-heterogeneity"),
    "model": "dhi",
    "parameters": asdict(DHIConfig(nbins=32, win_lcv=5)),
    "input_spacing_mm": [1, 1, 1],
}
Path("run_config.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
```

当前不会自动保存完整实验来源信息；建议同时记录输入清单、代码提交、预处理参数及依赖版本。
