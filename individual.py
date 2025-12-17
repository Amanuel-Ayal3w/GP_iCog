"""Individual representation for Sudoku GES."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from puzzle import Grid


@dataclass(slots=True)
class Individual:
    grid: Grid
    complexity: int = 0
    conflicts: int = 0
    fitness: float = 0.0

    def clone(self) -> "Individual":
        return Individual([row[:] for row in self.grid], self.complexity, self.conflicts, self.fitness)

    def signature(self) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(row) for row in self.grid)
