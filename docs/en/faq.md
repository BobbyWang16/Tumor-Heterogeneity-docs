# Frequently asked questions

## Why do the installation and import names differ?

The distribution is named `tumor-heterogeneity`, but setuptools currently packages `src*`. Use `from src.models import DHIModel`. A migration to `tumor_heterogeneity` is planned in [Package design](package-design.md); that import is not available yet.

## Why is my score NaN, zero, or missing?

Check that the mask is nonempty, the ROI is large enough, intensities are finite, and filenames match. Then inspect `features`, `details`, and the CSV `error` column. Models handle small ROIs differently. Do not silently replace NaN with zero.

## Can I pass raw images directly to compute?

The interface accepts arrays without reading spacing, registering, or standardizing resolution. Spatial models currently assume unit spacing; use 1 mm isotropic data for joint comparison. Same-shaped arrays can still represent different physical locations.

## Why does preprocessing fail with OrientImageFilter?

`src/core/preprocess_pipeline.py` currently calls `sitk.OrientImageFilter()`, which is absent in the locally verified SimpleITK 2.5.5 environment. Direction handling still needs a compatibility fix and geometry regression tests. A successful `--help` check is not an end-to-end preprocessing test.

The function also copies CT metadata to the mask, which is not equivalent to resampling or registration. Start with independently verified and spatially aligned preprocessed images. This documentation work does not change that algorithm.

## How do I run only one model without visualization?

```bash
python run_all_scores.py --dataset demo --models dhi --no-visualize
```

In Python, use `DHIModel().compute(image, mask)`.

## Why can THI and ITH-FS be slow?

THI computes local voxel features; ITH-FS computes multi-scale features, a neighbor graph, and eigenvectors. ROI size affects time and memory. Validate a small subset before running the cohort. GPU acceleration and case-level parallel processing are not currently promised.

## Where are the 3D label maps?

In the `compute()` result for models that provide them. Batch exports keep table fields to control memory and do not automatically save spatial maps.

## Is this equivalent to PyRadiomics or the original ITHscore?

No. Documentation organization is inspired by PyRadiomics, while methods and interfaces must be assessed individually. `ITHscore/` is a separate reference repository. QuanTAV's Python skeletonization is not claimed to match the MATLAB implementation value for value.

## How should I cite this software, and what is its license?

The repository root currently lacks a formal `LICENSE` file. The former README's MIT statement does not replace a complete license. Before a formal package release, clarify the core license and third-party attribution; the separate ITHscore license does not automatically cover the main package.

A verified publication citation for this software is not supplied. Record the version, commit, and settings, and cite the original publications for the methods you actually use. Do not cite the original ITHscore paper as if it described every implementation in this repository.
