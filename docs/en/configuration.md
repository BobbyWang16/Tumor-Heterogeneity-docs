# Configuration

Models currently use Python dataclasses. A unified YAML parameter file is not implemented.

## Configure one model

```python
from dataclasses import asdict
from src.core import DHIConfig
from src.models import DHIModel

config = DHIConfig(clip_percentiles=(1, 99), nbins=32, win_lcv=5)
model = DHIModel(config)
print(asdict(config))
# Once image and mask are ready: result = model.compute(image, mask)
```

## Common parameters

| Model | Configuration | Parameters used by the calculation | Defaults |
| --- | --- | --- | --- |
| DHI | `DHIConfig` | `clip_percentiles`, `nbins`, `win_lcv` | `(1, 99)`, `64`, `3` |
| HAB | `HABConfig` | `k_habitat`, `hu_min`, `hu_max` | `4`, `-1000`, `400` |
| PTH | `PTHConfig` | `ring_mm`, `target_block_size_mm3`, `compactness` | `5.0`, `5000`, `15.0` |
| SHI | `SHIConfig` | `scales` | `[1, 2, 4, 8, 16]` |
| THI | `THIConfig` | `k`, `padding`, `clip`, `n_workers` | `3`, `2`, `(1, 99)`, `4` |
| ITH-FS | `ITHFusionConfig` | `n_clusters`, `scales`, `n_neighbors` | `6`, `[1, 2, 3]`, `20` |

Some declared fields are not connected to their corresponding calculations, including `BIHConfig.box_sizes`, `SHIConfig.target_spacing`, and `ITHFusionConfig.adaptive_k/use_hog`. Do not assume changing them changes the algorithm. `save_intermediates` does not currently enable automatic map export.

## Custom configuration for a cohort

`ModelRunner` currently creates default model instances. For custom settings, use a model directly:

```python
from src.core import DataConfig, DHIConfig
from src.models import DHIModel

data = DataConfig(dataset="demo", data_root="./data", output_root="./results")
model = DHIModel(DHIConfig(nbins=32, win_lcv=5))
csv_path = model.run_and_save(data)
```

Rerunning the same output path overwrites the CSV. Use distinct `output_root` values or `csv_name` arguments for parameter comparisons.

## Save an experiment configuration

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

Complete provenance is not saved automatically. Also record input files, the code commit, preprocessing settings, and dependency versions.
