"""Configuration values for the Sudoku GES solver."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence


@dataclass(slots=True)
class Config:
    """Holds all tunable parameters for the search."""

    N: int = 3
    symbols: Sequence[int] | None = None
    pop_size: int = 200
    generations: int = 200
    p_cx: float = 0.9
    p_mut: float = 0.2
    elite: int = 2
    tourn_k: int = 3
    lam: float = 0.1
    seed: int | None = 42
    history_stride: int = 1

    def __post_init__(self) -> None:
        if self.N < 2:
            raise ValueError("N must be >= 2")
        n2 = self.N * self.N
        if self.symbols is None:
            self.symbols = tuple(range(1, n2 + 1))
        if len(self.symbols) != n2:
            raise ValueError("symbols length must equal N^2")
        if len(set(self.symbols)) != len(self.symbols):
            raise ValueError("symbols must be unique")
        if self.elite >= self.pop_size:
            raise ValueError("elite must be smaller than population size")
        if not 0.0 <= self.p_cx <= 1.0:
            raise ValueError("p_cx must be within [0, 1]")
        if not 0.0 <= self.p_mut <= 1.0:
            raise ValueError("p_mut must be within [0, 1]")
        if self.tourn_k < 2:
            raise ValueError("tourn_k must be >= 2")
        if self.history_stride < 1:
            raise ValueError("history_stride must be >= 1")

    @property
    def box_size(self) -> int:
        return self.N

    @property
    def grid_size(self) -> int:
        return self.N * self.N

    @property
    def symbol_list(self) -> List[int]:
        return list(self.symbols)
