# Development and documentation

This site builds from the public documentation-only repository `BobbyWang16/Tumor-Heterogeneity-docs`. Algorithm test commands below require access to the private implementation repository and must run from its root. Documentation build commands work in the public documentation repository.

## Local checks

```bash
python -m pip install -e ".[dev,survival,analysis]" -e ./QuanTAV
python -m pytest
python examples/quickstart.py
python QuanTAV/smoke_test.py
```

The full test suite includes QuanTAV and optional analysis dependencies, so installing only the core package is insufficient.

## Build the documentation

Documentation uses Sphinx, MyST Markdown, and the Read the Docs theme:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` for Chinese or `docs/_build/html/en/index.html` for English. The build does not import imaging algorithms or require research data. Read the Docs installs only documentation dependencies.

## Bilingual organization

Chinese pages live directly under `docs/`; matching English pages live under `docs/en/`. Both languages are generated in one build. The language link leads to the corresponding page instead of returning to the homepage.

This is one bilingual documentation project, not two Read the Docs translation projects. Search covers both languages; technical identifiers and examples stay consistent. Add both versions whenever a user-facing page changes.

## Writing and verification

- Keep the README focused on purpose, installation, a minimal example, and documentation links.
- Keep the first getting-started example independent of external downloads.
- Document implemented behavior in the user guide; place proposals in the package-design page.
- Explain the definition, units, assumptions, and edge cases when changing a feature.
- Do not describe unrun checks, unpublished packages, or unavailable capabilities as completed.

The private implementation repository’s root file `重构说明.md` is a maintenance record rather than a tutorial.
