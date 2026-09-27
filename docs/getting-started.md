# Getting Started

目标：先计算一个合成肿瘤的 DHI，再读取自己的 NIfTI 文件。首次示例使用 NumPy 生成数据，不需要临床表、下载影像或运行全部模型。

## 1. 第一次计算

安装主包后运行：

```python
import numpy as np
from src.core import DHIConfig
from src.models import DHIModel

rng = np.random.default_rng(42)
image = rng.normal(60, 15, size=(32, 32, 32)).astype(np.float32)
z, y, x = np.indices(image.shape)
mask = ((z - 16)**2 + (y - 16)**2 + (x - 16)**2 <= 9**2)

model = DHIModel(DHIConfig(nbins=64, win_lcv=3))
result = model.compute(image, mask)

assert np.isfinite(result["score"])
print("DHI:", round(result["score"], 4))
print("特征数:", len(result["features"]))
print("ROI 体素数:", result["details"]["n_voxels"])
```

运行后应得到有限的 DHI 分数、16 个特征及正的 ROI 体素数。DHI 的主分数为 ROI 灰度变异系数，不是疾病概率，也不是七模型的平均分。

本地验证结果为 `DHI: 0.2271`、16 个特征、3071 个 ROI 体素。不同依赖版本可能出现小的数值差异。

同一示例已保存为 `examples/quickstart.py`，在仓库根目录执行：

```bash
python examples/quickstart.py
```

## 2. 读取自己的 CT 与掩膜

以下代码需要替换成实际存在、已对齐的文件路径：

```python
import numpy as np
from src.core import load_image, load_seg
from src.models import DHIModel

image, image_meta = load_image("data/demo/image_process/case001.nii.gz")
mask, mask_meta = load_seg("data/demo/mask_process/case001.nii.gz")

assert image.ndim == mask.ndim == 3
assert image.shape == mask.shape
assert mask.any()
assert np.isfinite(image).all()
assert np.allclose(image_meta.GetSpacing(), mask_meta.GetSpacing())
assert np.allclose(image_meta.GetOrigin(), mask_meta.GetOrigin())
assert np.allclose(image_meta.GetDirection(), mask_meta.GetDirection())

result = DHIModel().compute(image, mask)
print(result["score"])
```

SimpleITK 读取后的数组顺序是 `(z, y, x)`；`GetSpacing()` 返回 `(x, y, z)`。`load_seg()` 将所有正标签合并成前景，如需单个标签，应先自行选取。

上述检查确认几何属性一致，不能替代配准质量检查。主模型的 `compute()` 不接收图像元数据，也不会自动重采样。运行全部模型前，按 [数据要求](data-and-batch.md) 准备 1 mm 各向同性数据。

## 3. 选择多个模型

在已有 `image`、`mask` 的基础上：

```python
from src.models import get_model

results = {
    name: get_model(name)().compute(image.copy(), mask.copy())
    for name in ["bih", "dhi"]
}
scores = {name: result["score"] for name, result in results.items()}
print(scores)
```

`get_model()` 返回模型类；再调用 `()` 创建实例。建议先用 BIH、DHI 检查流程，再启用耗时更多的 THI、ITH-FS。

示例使用数组副本，避免某些模型对工作数组的原地处理影响后续模型。

## 4. 导出特征表

继续使用第 1 步的 `result`：

```python
import pandas as pd

row = {"case_id": "synthetic", "score": result["score"]}
row.update({f"feat_{name}": value for name, value in result["features"].items()})
pd.DataFrame([row]).to_csv("synthetic_dhi.csv", index=False)
```

这个文件包含一行病例记录。队列批量导出使用 [ModelRunner](data-and-batch.md)，无需自己循环读文件。
