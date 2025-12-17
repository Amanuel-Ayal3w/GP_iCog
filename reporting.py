"""Reporting helpers for Sudoku GES runs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List

from .puzzle import pretty_print


def save_run_csv(history: Iterable[Dict[str, int]], path: str | Path) -> None:
    path = Path(path)
    fieldnames = ["generation", "best_conflicts", "best_complexity", "best_fitness"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in history:
            writer.writerow(row)


def save_best_solution(best: Dict[str, object], path: str | Path) -> None:
    path = Path(path)
    grid = best.get("grid")
    if grid is None:
        raise ValueError("best result missing grid")
    text = pretty_print(grid)
    with path.open("w") as f:
        f.write(text)
        f.write("\n")
