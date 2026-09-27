# Python package release design

This page describes a **proposal**, not an implemented API. User-guide examples use current interfaces.

## Naming and responsibilities

Keep `tumor-heterogeneity` as the proposed distribution name and migrate the import namespace to `tumor_heterogeneity`. This describes the domain and avoids confusion with the third-party ITHscore package. PyPI name availability must be checked before publication.

```text
pyproject.toml
src/
└── tumor_heterogeneity/
    ├── __init__.py
    ├── extractor.py       # User-facing extraction interface
    ├── config.py          # Parameters and validation
    ├── io.py              # Images and physical metadata
    ├── preprocessing.py
    ├── models/            # Seven models
    ├── pipeline/          # Cohort execution
    ├── visualization/
    └── survival/
examples/
tests/
docs/
```

Here `src/` becomes a source-layout directory rather than the public import name.

## Proposed extraction interface

This example is a design sketch and cannot run yet:

```python
# Proposed API — not implemented
from tumor_heterogeneity import HeterogeneityExtractor

extractor = HeterogeneityExtractor(models=["bih", "dhi"])
result = extractor.execute("image.nii.gz", "mask.nii.gz")
```

The extractor should handle geometry checks, preprocessing, model settings, errors, and provenance. Lower-level array interfaces should remain available for method development.

A proposed result contains `scores`, `features`, `maps`, and `diagnostics`. Map export must preserve origin, direction, and spacing. Case and cohort processing should share a defined result schema.

## Relationships between subprojects

| Component | Proposed role |
| --- | --- |
| Seven ITH models | Core package |
| QuanTAV | Keep separate `quantav-py`; integrate later through an adapter |
| DualCT | Integrate after stabilizing inputs, results, and metadata; it currently processes CT phases, not automatically dual-energy CT |
| Gene and R analysis | Research workflows/examples, not core import dependencies |
| Third-party ITHscore | Preserve its source and license separately rather than bundling it without review |

Do not include datasets, result archives, R workspaces, or nested Git repositories in the installed package.

## Release sequence

1. Unify version sources and migrate imports with a compatibility policy.
2. Fix preprocessing orientation and validate physical CT/mask geometry.
3. Remove or implement unused settings and define stable result and parameter contracts.
4. Add an installed CLI with consistent paths, logs, and exit codes.
5. Verify wheel/sdist installation and examples in fresh environments; establish a support matrix.
6. Define the core license, third-party attribution, and citation guidance.
7. Publish versioned documentation and then decide on a PyPI release.

Documentation hosting is independent of PyPI publication. `.readthedocs.yaml` configures the documentation build; it does not publish Python distributions.
