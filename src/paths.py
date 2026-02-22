from __future__ import annotations
import os
from pathlib import Path

def project_root() -> Path:
    """
    Resolve repository root. Works both locally and in Airflow.
    Priority:
      1) PIPELINE_ROOT env var
      2) directory two levels above this file (repo/src/paths.py -> repo/)
    """
    env = os.getenv("PIPELINE_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[1]

def data_dir() -> Path:
    return project_root() / "data"

def raw_dir() -> Path:
    return data_dir() / "raw"

def processed_dir() -> Path:
    return data_dir() / "processed"

def marts_dir() -> Path:
    return data_dir() / "marts"

def assets_dir() -> Path:
    return project_root() / "assets"

def reports_dir() -> Path:
    return project_root() / "reports"
