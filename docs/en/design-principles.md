# Why is it designed this way?

Our central idea is to **describe the same tumor from several interpretable perspectives, with inputs and outputs that can be inspected at each step**.

## 1. Seven models ask different questions

| Question | Perspective | Model |
| --- | --- | --- |
| How spread out are intensity values? | Value distribution | DHI |
| How does the signal pattern change with observation scale? | Multi-scale slice structure | BIH |
| What are the shape, surface, and filling characteristics? | 3D geometry | SHI |
| Which image regions coexist, and how do they mix? | Habitats and spatial relationships | HAB |
| Are similar local textures fragmented? | Texture and connectivity | THI |
| How different are blocks of tissue around the tumor? | Peritumoral environment | PTH |
| How are regions organized when features and distance are combined? | Joint feature and spatial relationships | ITH-FS |

These perspectives complement each other but are not guaranteed to be statistically independent. The aim is to compare different descriptions, rather than simply accumulate more scores.

## 2. Share an interface without hiding differences

Models share `compute(image, mask)` and the basic `score` and `features` result fields. Switching a model does not require rewriting the input code.

Spatial maps remain optional. An intensity summary does not naturally define a partition map, so we do not force every model to produce one. Batch processing retains table fields rather than storing an entire cohort's 3D arrays in memory.

This consistency currently exists at the model layer. A higher-level extractor with geometry checks and unified configuration is still part of the [release design](package-design.md).

## 3. Make inputs comparable before comparing scores

A five-voxel ring has a different physical width in 1 mm and 3 mm images. Several current models assume unit spacing, so whole-model experiments should first prepare 1 mm isotropic images.

That does not remove the need to choose preprocessing for the study. Record acquisition conditions, interpolation, intensity clipping, mask processing, and inclusion rules. The model interface does not perform registration for you.

## 4. How the numbers are calculated

### DHI: start with relative variation

The main score is approximately:

`CV = standard deviation / mean`

The implementation retains intensities within configured percentiles, uses the sample standard deviation, and adds a small denominator offset. Local CV statistics are also returned as features but are not automatically combined into the main score. Because HU means can be negative or close to zero, interpret CV alongside the mean.

### BIH: change the observation scale

The implementation selects the largest axial tumor slice and normalizes ROI intensities. At each box scale, it summarizes the average signal of foreground-containing boxes. A log–log fit supplies the negative slope reported as `fd`. This is the implementation's signal-scale descriptor, not a claim of equivalence to every classical binary box-counting method. Inspect `r2` and residuals to assess the fit.

### HAB: consider both composition and arrangement

GMM and spatial priors produce image habitats. The score combines composition entropy, radial layering, core–shell differences, boundary and global mixing, and fragmentation. `H_HAB` uses fixed hand-selected weights and is clipped to `[0, 1]`; these are not clinical risk coefficients learned from the current cohort.

### THI: do similar textures form coherent regions?

THI extracts local features and applies KMeans. For each cluster, it computes the fraction occupied by its largest connected component. The score is one minus the average fraction across clusters. Fragmenting a cluster usually reduces that largest-component fraction.

### PTH: examine the surrounding tissue

A peritumoral ring is partitioned using SLIC, and block-level features are compared. The main score averages `PTH_CV_*` features. Input images must retain surrounding tissue; insufficient rings can produce empty features and fallback scores.

### SHI: describe the boundary and shape

Outputs include volume, surface area, sphericity, convex-hull measurements, and fractal descriptors. The current main score averages available values of `1-sphericity`, `1-solidity`, and `FD_surface/3`. It is a hand-composed shape summary, not a calibrated biological heterogeneity scale.

### ITH-FS: combine feature similarity with spatial proximity

Multi-scale voxel features define a nearest-neighbor graph. Edge weights account for both feature and spatial distances. Spectral clustering produces regions, and connected-region structure and spatial coherence contribute to the score. “Fusion” refers to features and spatial relationships, not averaging the other six scores.

The `confidence_map` reflects relative distances from voxels to their cluster centers in spectral space. It measures internal consistency rather than calibrated probability.

## 5. Interpretation still requires inspection

Different structures can produce similar scores. Check inputs and errors first, then inspect features, fit quality, and regional maps before interpreting cohort differences. We retain these intermediate descriptions so the result can be traced beyond a single number.

Complete experiment configuration still needs to be saved explicitly. Automatic provenance, a unified high-level API, and configuration cleanup remain planned. See [Configuration](configuration.md) and [Models and outputs](models.md).
