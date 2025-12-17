"""Mutation operators preserving grammar constraints."""

from __future__ import annotations

import random

from config import Config
from grammar import apply_givens, box_cells, check_boxes, check_givens
from individual import Individual
from puzzle import Mask


def mut_swap_in_box(individual: Individual, cfg: Config, givens: list[list[int]], mask: Mask, rng: random.Random) -> Individual:
    child = individual.clone()
    total_boxes = cfg.N * cfg.N
    box_indices = list(range(total_boxes))
    rng.shuffle(box_indices)

    for box_index in box_indices:
        coords = [(r, c) for r, c in box_cells(box_index, cfg.N) if not mask[r][c]]
        if len(coords) < 2:
            continue
        (r1, c1), (r2, c2) = rng.sample(coords, 2)
        child.grid[r1][c1], child.grid[r2][c2] = child.grid[r2][c2], child.grid[r1][c1]
        child.complexity += 1
        apply_givens(child.grid, givens, mask)
        if not check_boxes(child.grid, cfg.N, cfg.symbols):
            raise AssertionError("mutation broke box constraint")
        if not check_givens(child.grid, givens, mask):
            raise AssertionError("mutation broke givens")
        return child
    return child
