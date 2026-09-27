# API Reference

本页列出推荐入口；签名以当前源码为准。`src` 是当前实际导入名。

## 模型

### `src.models.get_model(name)`

返回模型类，支持 `bih`、`dhi`、`hab`、`pth`、`shi`、`thi`、`ith_fusion`。未知名称抛出 `ValueError`。

### `Model(config=None).compute(image, mask)`

`image`、`mask` 为三维 NumPy 数组；模型配置是对应 dataclass。返回结果字典，字段见 [模型与输出](models.md)。

### `Model.batch_compute(data_cfg, limit=None)`

读取配对病例并返回 `pandas.DataFrame`，不写文件。病例异常记录到表中；没有匹配病例时返回空表。`limit` 建议使用正整数。

### `Model.run_and_save(data_cfg, csv_name=None)`

计算并写入 `{output_root}/{dataset}/{model}/{model}_{dataset}.csv`，返回路径字符串。`csv_name` 可覆盖文件名。无病例或整批无有限分数时抛出异常；后者保留诊断 CSV。

## 数据与队列

### `src.core.DataConfig`

```python
from src.core import DataConfig

config = DataConfig(
    dataset="demo",
    data_root="./data",
    use_processed=True,
    output_root="./results",
    image_suffix=".nii.gz",
    mask_suffix=".nii.gz",
)
```

提供 `image_dir`、`mask_dir`、`output_dir` 路径属性。文件匹配及目录回退行为见 [批处理](data-and-batch.md)。

### `src.core.DatasetLoader`

主要接口：`pairs`、`load_case(case_id)`、`clinical`、`get_survival_data()`、`get_observer_mask_dirs()`。`load_case()` 返回两个数组，不返回空间元数据。

### `src.pipeline.ModelRunner(data_cfg, models=None)`

- `run(visualize=False)`：返回 `{model_name: csv_path}`。
- `run_single(model_name, visualize=False)`：返回该模型 CSV 路径。

`visualize=True` 从输出表生成可视化；不代表把每例标签图写入 NIfTI。

## 图像读取

### `src.core.load_image(path)`

返回 `(array, sitk_image)`。文件路径由 SimpleITK 读取，也支持 DICOM 系列目录。批处理配对接口默认面向 NIfTI 文件。

### `src.core.load_seg(path)`

返回 `(binary_array, sitk_image)`，以 `array > 0` 合并前景。

## 报告

- `src.visualization.generate_algorithm_diagnostics(dataset_name, results_dir, out_dir)`：从模型结果表生成队列诊断。
- `src.survival.generate_survival_report(dataset_name, data_root, results_dir, out_dir, models=None)`：输出病例对齐后的生存探索报告，需要 `survival` 依赖。

## QuanTAV 独立接口

安装 `./QuanTAV` 后使用；以下文件路径需替换为自己的配准数据：

```python
from quantav_py import QuantavParams, analyze_case

result = analyze_case(
    image=None,
    tumor_mask="tumor.nii.gz",
    vessel_mask="vessels.nii.gz",
    params=QuantavParams(create_visualizations=False),
    output_dir="quantav_output",
    case_id="case001",
)
features = result.as_dict()
print(len(features))
```

NumPy 数组可以代替文件路径；数组与 NPY 的间距通过 `QuantavParams(spacing=(z_mm, y_mm, x_mm))` 显式传入。图像文件会优先使用文件间距，来源间距不一致时报错。
