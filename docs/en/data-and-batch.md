# Data and batch processing

## Input conventions

- Use a finite 3D CT array in HU and a nonempty, same-shaped 3D foreground mask.
- CT and mask must already share size, spacing, origin, direction, and anatomical alignment.
- Current HAB, PTH, SHI, and other spatial implementations assume unit voxel spacing. Prepare **1 × 1 × 1 mm** data before comparing all models. A configuration field does not imply automatic resampling.
- PTH needs surrounding tissue. Do not crop tightly to the tumor boundary.
- Apply consistent preprocessing across cases and record clipping, resampling, and model settings.

## Directory layout

```text
data/
└── demo/
    ├── image/                  # Original CT
    │   └── case001.nii.gz
    ├── mask/                   # Original segmentation
    │   └── case001.nii.gz
    ├── image_process/          # Preprocessed CT
    │   └── case001.nii.gz
    ├── mask_process/           # Preprocessed segmentation
    │   └── case001.nii.gz
    └── clinical.xlsx           # Optional; required for survival exploration
```

Prefer identical case filenames for image and mask. The default suffix is `.nii.gz`. The matcher also removes markers such as `_ct` and `_mask`, which can merge IDs containing those substrings. Inspect matching before running a cohort:

```python
from src.core import DatasetLoader

loader = DatasetLoader("demo", data_root="./data")
print("Matched cases:", len(loader.pairs))
print(loader.pairs[:3])
```

When both processed directories exist, they take priority; otherwise Python data configuration falls back to `image/` and `mask/`. Existing directories do not guarantee complete data. Unmatched files are not scored.

## Batch processing in Python

```python
from src.core import DataConfig
from src.pipeline import ModelRunner

config = DataConfig(dataset="demo", data_root="./data", output_root="./results")
paths = ModelRunner(config, models=["bih", "dhi"]).run(visualize=False)
print(paths)
```

Output:

```text
results/demo/
├── bih/bih_demo.csv
└── dhi/dhi_demo.csv
```

`models=None` selects all models; `models=[]` selects none. CSV files retain scores, features, and scalar details rather than 3D maps. Case exceptions appear in `error`; no cases or an entire batch without finite scores raises an exception.

## Command line

Run the repository scripts from its root. An installed `ith` console command is not implemented yet.

```bash
python run_all_scores.py --dataset demo --models bih dhi --no-visualize
python run_all_scores.py --dataset demo --models bih dhi --visualize
```

The CLI checks for processed directories by default. `--skip-preprocess-check` only skips that check; it does not preprocess or validate geometry. `--no-visualize` overrides the script's visualization default.

The repository includes `scripts/preprocess_all.py`, but its direction handling has a current SimpleITK API compatibility issue described in [FAQ](faq.md). Start with independently verified 1 mm images. Directory existence is not evidence of successful preprocessing.

## Survival exploration

`clinical.xlsx` requires `PatientID` or `case_id`, `time`, and `event`. Use a consistent time unit, 0/1 event coding, and case IDs matching image filenames.

```bash
python -m pip install -e ".[survival]"
python run_all_scores.py --dataset demo --models bih dhi --no-visualize --survival
```

Reports join by case ID, fit univariate Cox models, and split KM groups at the median. This is not multivariable model training, independent validation, or automatic clinical risk stratification.
