"""Fitness evaluation with complexity penalty."""

from __future__ import annotations

from collections import Counter

from config import Config
from individual import Individual
from puzzle import Grid


def conflicts(grid: Grid, cfg: Config) -> int:
    dup_count = 0
    size = cfg.grid_size

    for row in grid:
        dup_count += _duplicate_count(row)

    for c in range(size):
        column = [grid[r][c] for r in range(size)]
        dup_count += _duplicate_count(column)

    return dup_count


def score(individual: Individual, cfg: Config) -> Individual:
    individual.conflicts = conflicts(individual.grid, cfg)
    individual.fitness = -individual.conflicts - cfg.lam * individual.complexity
    return individual


def better(a: Individual, b: Individual) -> bool:
    if a.conflicts != b.conflicts:
        return a.conflicts < b.conflicts
    if a.complexity != b.complexity:
        return a.complexity < b.complexity
    return a.fitness > b.fitness


def _duplicate_count(values: list[int]) -> int:
    counter = Counter(values)
    total = 0
    for val, count in counter.items():
        if val == 0:
            continue
        if count > 1:
            total += count - 1
    return total
