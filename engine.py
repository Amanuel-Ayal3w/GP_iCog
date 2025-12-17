"""Evolutionary engine coordinating the Sudoku GES search."""

from __future__ import annotations

import random
from typing import Any, Dict, Iterable, List, Tuple

from config import Config
from fitness import better, score
from grammar import is_valid_individual
from init_population import init_population
from ops.crossover import cx_boxes
from ops.mutation import mut_swap_in_box
from ops.replacement import elitist_generational
from ops.selection import tournament
from puzzle import parse_grid, validate_givens


def run(cfg: Config, puzzle_input: str | Iterable[Iterable[int]]) -> Tuple[Any, List[Dict[str, Any]]]:
    size = cfg.grid_size
    givens, mask = parse_grid(puzzle_input, size)
    validate_givens(givens, mask, cfg.symbols)

    rng = random.Random(cfg.seed)
    population = init_population(cfg, givens, mask)
    for ind in population:
        score(ind, cfg)

    history: List[Dict[str, Any]] = []
    best = min(population, key=_sort_key)

    for generation in range(cfg.generations + 1):
        if generation % cfg.history_stride == 0:
            history.append(
                {
                    "generation": generation,
                    "best_conflicts": best.conflicts,
                    "best_complexity": best.complexity,
                    "best_fitness": best.fitness,
                }
            )
        if best.conflicts == 0:
            break
        offspring: List[Any] = []
        while len(offspring) < cfg.pop_size:
            parent1 = tournament(population, cfg, rng)
            parent2 = tournament(population, cfg, rng)
            child1, child2 = parent1.clone(), parent2.clone()
            if rng.random() < cfg.p_cx:
                child1, child2 = cx_boxes(parent1, parent2, cfg, givens, mask, rng)
            if rng.random() < cfg.p_mut:
                child1 = mut_swap_in_box(child1, cfg, givens, mask, rng)
            if rng.random() < cfg.p_mut:
                child2 = mut_swap_in_box(child2, cfg, givens, mask, rng)
            score(child1, cfg)
            score(child2, cfg)
            offspring.append(child1)
            if len(offspring) < cfg.pop_size:
                offspring.append(child2)
        population = elitist_generational(population, offspring, cfg)
        for ind in population:
            score(ind, cfg)
        best = min(population, key=_sort_key)

    best_grid = [row[:] for row in best.grid]
    if not is_valid_individual(best_grid, givens, mask, cfg.N, cfg.symbols):
        raise AssertionError("best individual is invalid")
    return {
        "grid": best_grid,
        "conflicts": best.conflicts,
        "complexity": best.complexity,
        "fitness": best.fitness,
    }, history


def _sort_key(ind) -> tuple[int, int, float]:
    return (ind.conflicts, ind.complexity, -ind.fitness)
