# Getting Started

Start by calculating DHI for a synthetic tumor, then load your own NIfTI files. The first example does not need downloaded images, a clinical table, or all seven models.

## 1. Your first calculation

After installing the core package, run:

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
print("Features:", len(result["features"]))
print("ROI voxels:", result["details"]["n_voxels"])
```

The locally verified output is:

```text
DHI: 0.2271
Features: 16
ROI voxels: 3071
```

Minor numerical differences may occur across dependency versions. DHI summarizes intensity variation; it is neither a disease probability nor an average of seven models.

The same example is saved as `examples/quickstart.py`:

```bash
python examples/quickstart.py
```

## 2. Read your CT and mask

Replace the following paths with existing, aligned files:

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

SimpleITK arrays use `(z, y, x)` order; `GetSpacing()` returns `(x, y, z)`. `load_seg()` combines all positive labels into foreground. Select a label yourself if only one label should be analyzed.

These checks confirm matching geometry, not registration quality. `compute()` does not receive metadata or resample automatically. Prepare 1 mm isotropic data before running all models; see [input requirements](data-and-batch.md).

## 3. Select several models

With `image` and `mask` already prepared:

```python
from src.models import get_model

results = {
    name: get_model(name)().compute(image.copy(), mask.copy())
    for name in ["bih", "dhi"]
}
scores = {name: result["score"] for name, result in results.items()}
print(scores)
```

`get_model()` returns a class; the following `()` creates an instance. Array copies keep models that modify their working input from affecting subsequent calculations. Start with BIH and DHI before enabling more expensive THI and ITH-FS calculations.

## 4. Export a feature table

Using the DHI `result` from step 1:

```python
import pandas as pd

row = {"case_id": "synthetic", "score": result["score"]}
row.update({f"feat_{name}": value for name, value in result["features"].items()})
pd.DataFrame([row]).to_csv("synthetic_dhi.csv", index=False)
```

The file contains one case. For a cohort, use [ModelRunner](data-and-batch.md) rather than writing your own file loop.
