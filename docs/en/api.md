# API Reference

These are the recommended entry points. Current source code is authoritative for signatures; `src` is the actual import namespace.

## Models

### `src.models.get_model(name)`

Returns a model class. Supported names are `bih`, `dhi`, `hab`, `pth`, `shi`, `thi`, and `ith_fusion`. Unknown names raise `ValueError`.

### `Model(config=None).compute(image, mask)`

Accepts 3D NumPy image and mask arrays with an optional model-specific dataclass. Returns the dictionary described in [Models and outputs](models.md).

### `Model.batch_compute(data_cfg, limit=None)`

Processes paired cases and returns a `pandas.DataFrame` without writing a file. Case exceptions are recorded in the table; no pairs produces an empty table. Use a positive integer for `limit`.

### `Model.run_and_save(data_cfg, csv_name=None)`

Writes `{output_root}/{dataset}/{model}/{model}_{dataset}.csv` and returns its path. `csv_name` overrides the filename. No cases or no finite scores raises an exception; the latter retains the diagnostic CSV.

## Data and cohorts

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

Exposes `image_dir`, `mask_dir`, and `output_dir`. See [batch processing](data-and-batch.md) for directory selection and matching.

### `src.core.DatasetLoader`

Key interfaces: `pairs`, `load_case(case_id)`, `clinical`, `get_survival_data()`, and `get_observer_mask_dirs()`. `load_case()` returns two arrays without spatial metadata.

### `src.pipeline.ModelRunner(data_cfg, models=None)`

- `run(visualize=False)` returns `{model_name: csv_path}`.
- `run_single(model_name, visualize=False)` returns one model's CSV path.

`visualize=True` generates figures from output tables. It does not export each case's label map as NIfTI.

## Image input

### `src.core.load_image(path)`

Returns `(array, sitk_image)`. SimpleITK reads image files; DICOM series directories are also accepted. Default cohort matching expects NIfTI files.

### `src.core.load_seg(path)`

Returns `(binary_array, sitk_image)`, combining positive values into foreground.

## Reports

- `src.visualization.generate_algorithm_diagnostics(dataset_name, results_dir, out_dir)` generates cohort diagnostics from score tables.
- `src.survival.generate_survival_report(dataset_name, data_root, results_dir, out_dir, models=None)` generates case-aligned survival exploration reports; requires the `survival` extra.

## Separate QuanTAV interface

Install `./QuanTAV`, then replace these paths with aligned data:

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

NumPy arrays may replace paths. Set array and NPY spacing explicitly with `QuantavParams(spacing=(z_mm, y_mm, x_mm))`. Image file metadata takes precedence for file inputs, and inconsistent source spacings raise an error.
