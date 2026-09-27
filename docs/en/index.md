# Tumor Heterogeneity

**One tumor. More than one way to understand it.**

```{raw} html
<div class="ith-hero"><p><strong>Start with a CT image and a tumor mask.</strong><br>Describe how intensities vary, how regions are arranged, and what the tumor boundary looks like using inspectable numbers and spatial maps.</p><p>Run one small example first. You do not need to learn all seven algorithms to get started.</p></div>
```

Tumor Heterogeneity is a Python toolkit for studying tumor heterogeneity in CT images. The core package provides seven scoring models, a shared case-level interface, cohort CSV export, and optional visualization and survival exploration.

- **New users:** [Installation](installation.md) → [Getting Started](getting-started.md).
- **Understand the ideas:** [Basic concepts](concepts.md) → [Design principles](design-principles.md).
- **Analyze your cohort:** [Data and batch processing](data-and-batch.md).
- **Interpret the results:** [Models and outputs](models.md) → [Configuration](configuration.md).
- **Integrate or contribute:** [API Reference](api.md) → [Package design](package-design.md).

## See heterogeneity

![Synthetic image, tumor mask, illustrative partitions and surrounding ring](../_static/figures/workflow-en.png)

**Educational simulation, not patient imaging or model predictions.** Explore the [visual guide](visual-guide.md) to understand intensity distributions and spatial arrangement.

## From input to result

```{raw} html
<div class="ith-flow" aria-label="Analysis workflow">
<div><strong>01 · Prepare</strong><small>The CT supplies intensities; the mask defines the region.</small></div>
<div><strong>02 · Align</strong><small>Check coordinates and resolution before comparing cases.</small></div>
<div><strong>03 · Describe</strong><small>Choose intensity, shape, or spatial partition models.</small></div>
<div><strong>04 · Inspect</strong><small>Review scores, features, maps, and failed-case records.</small></div>
</div>
```

## What is available?

| Capability | Input | Output |
| --- | --- | --- |
| Case-level ITH calculation | CT array + binary mask | Score, features, and maps for some models |
| Cohort processing | Paired NIfTI files | One case-level CSV per model |
| Cohort diagnostics | Model CSV files | Distributions, agreement, and quality summaries |
| Survival exploration | Scores + clinical time/event table | Univariate Cox and KM curves |
| QuanTAV extension | Tumor and vessel masks | Vessel morphology and organization features; separate installation |

Start with **DHI** to understand intensity variability. Add **HAB / THI** to inspect regional organization, or **PTH** to examine tissue around the tumor. See [model selection](models.md).

The distribution is currently named `tumor-heterogeneity`, while the import namespace is still `src`. Source installation is supported; these instructions do not assume a PyPI release exists. DualCT, R workflows, and the third-party ITHscore repository have separate roles described in [Package design](package-design.md).

Every page links to its Chinese counterpart. [简体中文文档](../index.md).

```{toctree}
:maxdepth: 2
:caption: User guide

installation
concepts
visual-guide
getting-started
design-principles
data-and-batch
configuration
models
api
faq
```

```{toctree}
:maxdepth: 1
:caption: Development and release

package-design
contributing
```

## Documentation approach

The organization of installation, usage, configuration, features, and API sections is inspired by the [PyRadiomics documentation](https://pyradiomics.readthedocs.io/en/latest/). Content and examples describe this repository; this is not a PyRadiomics compatibility layer.
