"""Smoke test: run the full spaCy project workflow end to end.

Requires the project dependencies (see requirements.txt) and a fetched
``assets/`` directory. Run with ``pytest test_project.py``.
"""
from pathlib import Path

from spacy.cli.project.assets import project_assets
from spacy.cli.project.run import project_run


def test_textcat_project_workflow():
    root = Path(__file__).parent
    project_assets(root)
    project_run(root, "all", capture=True)
