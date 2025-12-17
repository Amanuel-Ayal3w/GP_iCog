"""Sudoku puzzle parsing and utility helpers."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Grid = List[List[int]]
Mask = List[List[bool]]


def parse_grid(data: str | Iterable[Sequence[int]], size: int) -> Tuple[Grid, Mask]:
    """Parse raw puzzle data into grid and mask."""

    values: List[List[int]] = []
    if isinstance(data, str):
        tokens = [ch for ch in data if not ch.isspace()]
        if len(tokens) != size * size:
            raise ValueError("string input does not match expected grid size")
        rows = [tokens[i : i + size] for i in range(0, len(tokens), size)]
        for row in rows:
            values.append([_parse_cell(cell) for cell in row])
    else:
        for row in data:
            row_list = list(row)
            if len(row_list) != size:
                raise ValueError("row length mismatch")
            values.append([int(v) for v in row_list])

    if len(values) != size:
        raise ValueError("grid height mismatch")

    mask: Mask = [[cell != 0 for cell in row] for row in values]
    return values, mask


def validate_givens(grid: Grid, mask: Mask, symbols: Sequence[int]) -> None:
    """Ensure givens obey the allowed symbol set."""

    allowed = set(symbols)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if mask[r][c] and cell not in allowed:
                raise ValueError(f"invalid given at ({r}, {c})")


def pretty_print(grid: Grid) -> str:
    """Return a readable string for logging or reports."""

    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def _parse_cell(token: str) -> int:
    if token in {"0", ".", "_"}:
        return 0
    try:
        return int(token)
    except ValueError as exc:
        raise ValueError(f"cannot parse cell value '{token}'") from exc
