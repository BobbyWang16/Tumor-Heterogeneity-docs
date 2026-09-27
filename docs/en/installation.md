# Installation

> The implementation repository is currently private. The source-installation steps below require repository access; a public PyPI installation is not yet available.

## Requirements

The core package declares Python ≥ 3.9. QuanTAV requires Python ≥ 3.10. The getting-started examples were verified on Python 3.11, which is recommended for a new environment.

## Install from source

```bash
git clone https://github.com/BobbyWang16/Tumor-Heterogeneity.git
cd Tumor-Heterogeneity
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install the core package:

```bash
python -m pip install -e .
```

Editable installation (`-e`) makes source changes available without reinstalling. These instructions do not assume a PyPI release or Conda channel exists.

## Optional dependencies

Run these commands from the repository root:

| Purpose | Command |
| --- | --- |
| Cox and Kaplan–Meier reports | `python -m pip install -e ".[survival]"` |
| Network dependency for gene-enrichment scripts | `python -m pip install -e ".[analysis]"` |
| Test tools | `python -m pip install -e ".[dev]"` |
| Documentation | `python -m pip install -e ".[docs]"` |
| QuanTAV vessel features | `python -m pip install -e ./QuanTAV` |

The `analysis` extra does not download expression data or install R/Bioconductor.

## Verify installation

```bash
python -c "from importlib.metadata import version; from src.models import MODEL_REGISTRY; print(version('tumor-heterogeneity')); print(list(MODEL_REGISTRY))"
```

Use installed package metadata and `pyproject.toml` as the version source. Continue to [your first calculation](getting-started.md).
