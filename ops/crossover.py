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
    if total_boxes == 0:
        return child1, child2

    indices = list(range(total_boxes))
    rng.shuffle(indices)
    # split shuffled box indices so child1 and child2 each inherit some boxes from both parents
    split = rng.randint(1, total_boxes - 1) if total_boxes > 1 else 0
    child1_p1_boxes = set(indices[:split])
    child2_p1_boxes = set(indices[split:]) if total_boxes > 1 else set()
    if total_boxes == 1:
        child1_p1_boxes = {indices[0]}
        child2_p1_boxes = set()

    for box in range(total_boxes):
        coords = box_cells(box, cfg.N)
        # child1 takes boxes from parent1 when present in child1_p1_boxes, otherwise from parent2
        source1 = parent1 if box in child1_p1_boxes else parent2
        # child2 does the complementary mix using child2_p1_boxes
        source2 = parent1 if box in child2_p1_boxes else parent2
        for r, c in coords:
            child1.grid[r][c] = source1.grid[r][c]
            child2.grid[r][c] = source2.grid[r][c]

    child1.complexity = int(round((parent1.complexity + parent2.complexity) / 2))
    child2.complexity = child1.complexity

    apply_givens(child1.grid, givens, mask)
    apply_givens(child2.grid, givens, mask)

    if not check_boxes(child1.grid, cfg.N, cfg.symbols) or not check_boxes(child2.grid, cfg.N, cfg.symbols):
        raise AssertionError("crossover produced invalid box")
    if not check_givens(child1.grid, givens, mask) or not check_givens(child2.grid, givens, mask):
        raise AssertionError("crossover broke givens")

    return child1, child2
