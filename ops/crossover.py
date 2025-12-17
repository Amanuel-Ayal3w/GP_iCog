"""Crossover operators constrained by Sudoku grammar."""

from __future__ import annotations

import random
from typing import Tuple

from config import Config
from grammar import apply_givens, box_cells, check_boxes, check_givens
from individual import Individual
from puzzle import Mask


def cx_boxes(parent1: Individual, parent2: Individual, cfg: Config, givens: list[list[int]], mask: Mask, rng: random.Random) -> Tuple[Individual, Individual]:
    child1 = parent1.clone()
    child2 = parent2.clone()

    total_boxes = cfg.N * cfg.N
    take_from_p1 = {box for box in range(total_boxes) if rng.random() < 0.5}
    if not take_from_p1:
        take_from_p1.add(rng.randrange(total_boxes))

    for box in range(total_boxes):
        coords = box_cells(box, cfg.N)
        source1 = parent1 if box in take_from_p1 else parent2
        source2 = parent2 if box in take_from_p1 else parent1
        for r, c in coords:
            child1.grid[r][c] = source1.grid[r][c]
            child2.grid[r][c] = source2.grid[r][c]

    child1.complexity = min(parent1.complexity, parent2.complexity)
    child2.complexity = min(parent1.complexity, parent2.complexity)

    apply_givens(child1.grid, givens, mask)
    apply_givens(child2.grid, givens, mask)

    if not check_boxes(child1.grid, cfg.N, cfg.symbols) or not check_boxes(child2.grid, cfg.N, cfg.symbols):
        raise AssertionError("crossover produced invalid box")
    if not check_givens(child1.grid, givens, mask) or not check_givens(child2.grid, givens, mask):
        raise AssertionError("crossover broke givens")

    return child1, child2
