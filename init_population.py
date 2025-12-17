"""Population initialization respecting Sudoku grammar."""

from __future__ import annotations

import random
from typing import List

from config import Config
from grammar import apply_givens, box_cells, check_boxes, check_givens, is_valid_individual
from individual import Individual
from puzzle import Grid, Mask


def init_individual(givens: Grid, mask: Mask, cfg: Config, rng: random.Random) -> Individual:
    size = cfg.grid_size
    candidate: Grid = [[0 for _ in range(size)] for _ in range(size)]
    apply_givens(candidate, givens, mask)

    total_boxes = cfg.N * cfg.N
    for b in range(total_boxes):
        coords = box_cells(b, cfg.N)
        present = {givens[r][c] for r, c in coords if mask[r][c]}
        missing = [s for s in cfg.symbols if s not in present]
        rng.shuffle(missing)
        idx = 0
        for r, c in coords:
            if mask[r][c]:
                candidate[r][c] = givens[r][c]
            else:
                candidate[r][c] = missing[idx]
                idx += 1
        if idx != len(missing):
            raise AssertionError("initializer did not consume all symbols")

    if not check_givens(candidate, givens, mask):
        raise AssertionError("initializer broke givens")
    if not check_boxes(candidate, cfg.N, cfg.symbols):
        raise AssertionError("initializer failed box validity")

    return Individual(candidate, complexity=0)


def init_population(cfg: Config, givens: Grid, mask: Mask) -> List[Individual]:
    rng = random.Random(cfg.seed)
    population = [init_individual(givens, mask, cfg, rng) for _ in range(cfg.pop_size)]
    return population
