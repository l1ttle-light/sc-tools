from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

DIRS = {
    "data_raw": ROOT / "data" / "raw",
    "data_interim": ROOT / "data" / "interim",
    "data_processed": ROOT / "data" / "processed",
    "fig_qc": ROOT / "results" / "figures" / "qc",
    "fig_umap": ROOT / "results" / "figures" / "umap",
    "tables_qc": ROOT / "results" / "tables" / "qc",
    "tables_markers": ROOT / "results" / "tables" / "markers",
    "reports": ROOT / "results" / "reports",
    "logs": ROOT / "logs",
}


def ensure_dirs() -> None:
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def load_params() -> dict[str, Any]:
    with (ROOT / "config" / "parameters.yaml").open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def step_path(name: str) -> Path:
    return DIRS["data_interim"] / name
