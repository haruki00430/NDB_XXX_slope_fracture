"""Shared helpers for public analysis scripts (UTF-8 stdout, typed scalars, config paths)."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


def configure_stdout_utf8() -> None:
    """Set Windows console to UTF-8 when supported (safe on other platforms)."""
    stdout = sys.stdout
    reconfigure = getattr(stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def as_float(value: Any) -> float:
    """Convert a regression coefficient or Series scalar to Python float."""
    if isinstance(value, (int, float, np.floating)):
        return float(value)
    return float(np.asarray(value).squeeze())


def as_series(column: pd.Series | pd.DataFrame) -> pd.Series:
    """Ensure a single DataFrame column is typed as Series for stats helpers."""
    if isinstance(column, pd.Series):
        return column
    squeezed = column.squeeze()
    if isinstance(squeezed, pd.Series):
        return squeezed
    return pd.Series(squeezed)


def resolve_project_path(project_root: Path, value: str | Path) -> Path:
    """Expand a config path relative to the project root when not absolute."""
    path = Path(value)
    return path.resolve() if path.is_absolute() else (project_root / path).resolve()


@dataclass(frozen=True)
class ProjectPaths:
    """Resolved filesystem paths for the manuscript mainline pipeline."""

    ndb_fracture_xlsx: Path
    ndb_walking_xlsx: Path
    census_csv: Path
    habitable_slope_csv: Path
    interim_dir: Path
    processed_dir: Path
    results_dir: Path
    bootstrap_replicates: int
    random_seed: int


def load_project_paths(project_root: Path) -> ProjectPaths:
    """
    Load paths from ``config/config.local.yaml`` (preferred) or ``config/config.yaml``.

    Copy ``config/config.yaml.example`` to ``config/config.local.yaml`` and edit paths
    before running the full NDB rebuild pipeline.
    """
    config_dir = project_root / "config"
    config_file: Path | None = None
    data: dict[str, Any] = {}
    for name in ("config.local.yaml", "config.yaml", "config.yaml.example"):
        candidate = config_dir / name
        if not candidate.exists():
            continue
        with open(candidate, encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
        if loaded.get("paths"):
            config_file = candidate
            data = loaded
            break
    if config_file is None:
        raise FileNotFoundError(
            "No configuration file with a 'paths' section found. Copy "
            "config/config.yaml.example to config/config.local.yaml and set "
            "paths to your NDB and census files (see DATA_SOURCES.md)."
        )

    paths = data.get("paths") or {}
    analysis = data.get("analysis") or {}

    required = (
        "ndb_fracture_xlsx",
        "ndb_walking_xlsx",
        "census_csv",
        "habitable_slope_csv",
        "interim_dir",
        "processed_dir",
        "results_dir",
    )
    missing = [key for key in required if not paths.get(key)]
    if missing:
        raise ValueError(
            f"Missing path keys in {config_file.name}: {', '.join(missing)}"
        )

    return ProjectPaths(
        ndb_fracture_xlsx=resolve_project_path(project_root, paths["ndb_fracture_xlsx"]),
        ndb_walking_xlsx=resolve_project_path(project_root, paths["ndb_walking_xlsx"]),
        census_csv=resolve_project_path(project_root, paths["census_csv"]),
        habitable_slope_csv=resolve_project_path(project_root, paths["habitable_slope_csv"]),
        interim_dir=resolve_project_path(project_root, paths["interim_dir"]),
        processed_dir=resolve_project_path(project_root, paths["processed_dir"]),
        results_dir=resolve_project_path(project_root, paths["results_dir"]),
        bootstrap_replicates=int(analysis.get("bootstrap_replicates", 5000)),
        random_seed=int(analysis.get("random_seed", 42)),
    )
