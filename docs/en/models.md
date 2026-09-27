# Models and outputs

## Seven ITH models

These scores measure different dimensions, with different scales and ranges. Do not average them directly or interpret them as a shared risk probability.

| Name | Method | Meaning of `score` | Spatial output |
| --- | --- | --- | --- |
| BIH | Signal-weighted box analysis on the largest axial tumor slice | Fitted `fd` | None |
| DHI | ROI intensity statistics and local CV | ROI intensity `CV` | None |
| HAB | GMM habitats with spatial priors | `H_HAB` | `label_map` |
| PTH | Peritumoral ring, SLIC blocks, and block variation | Mean of `PTH_CV_*` | `label_map` |
| SHI | Geometry, convex hull, fractals, and lacunarity | Mean of available `1-sphericity`, `1-solidity`, `FD_surface/3` | None |
| THI | Local voxel features and KMeans partitions | Cluster fragmentation | `label_map` |
| ITH-FS | Multi-scale features and spatial spectral clustering | Partition heterogeneity | `label_map`, `confidence_map` |

ITH-FS is a separate model, not a weighted combination of the other six scores. DHI divides by signed mean HU; negative or near-zero means affect interpretation. Do not treat score magnitude as a universal ranking across cohorts.

See [Design principles](design-principles.md) for the intuition and calculation behind each model.

## Case-level result

```text
result
├── score           Main score; float, possibly NaN
├── features        Model feature dictionary
├── details         Optional calculation details
├── label_map       Optional spatial partition
└── confidence_map  Optional internal ITH-FS confidence map
```

Not every model provides every field. Confidence is not calibrated clinical probability. Label numbers do not necessarily identify the same tissue across models or cases and must not be treated as pathology annotations.

Some degenerate HAB/PTH inputs return `score=0` and empty features. Inspect `features`, ROI size, and `details` before interpreting zero as low heterogeneity.

## Batch CSV columns

| Column | Meaning |
| --- | --- |
| `case_id` | Case ID matched from filenames |
| `score` | Main score |
| `feat_*` | Flattened model features |
| `detail_*` | Scalar calculation details |
| `error` | Exception text for failed cases, when present |

Missing fields become empty values. CSV export does not save 3D labels or confidence maps. Obtain those from case-level `compute()` results and preserve spatial metadata when saving them.

## QuanTAV

The separate QuanTAV package accepts an optional CT image plus tumor and vessel masks. `analyze_case()` returns a `FeatureResult` containing 91 features, branch information, and metadata. See [API Reference](api.md). This is a different result structure from the seven-model `score` dictionary.
