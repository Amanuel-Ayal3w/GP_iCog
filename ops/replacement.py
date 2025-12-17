"""Replacement strategies for generational evolution."""

from __future__ import annotations

from typing import Iterable, List

from config import Config
from fitness import better
from individual import Individual


def elitist_generational(population: List[Individual], offspring: Iterable[Individual], cfg: Config) -> List[Individual]:
    elite_sorted = sorted(population, key=_sort_key)
    elite = elite_sorted[: cfg.elite]
    children = list(offspring)
    combined = elite + children
    combined.sort(key=_sort_key)
    return combined[: cfg.pop_size]


def _sort_key(ind: Individual) -> tuple[int, int, float]:
    return (ind.conflicts, ind.complexity, -ind.fitness)
