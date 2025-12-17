"""Grammar-inspired constraints for Sudoku candidates."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

from puzzle import Grid, Mask


def box_cells(box_index: int, N: int) -> List[Tuple[int, int]]:
    """Return the coordinates within a subgrid."""

    side = N * N
    box_row = box_index // N
    box_col = box_index % N
    start_r = box_row * N
    start_c = box_col * N
    return [
        (start_r + dr, start_c + dc)
        for dr in range(N)
        for dc in range(N)
        if start_r + dr < side and start_c + dc < side
    ]


def check_givens(grid: Grid, givens: Grid, mask: Mask) -> bool:
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if mask[r][c] and value != givens[r][c]:
                return False
    return True


def check_boxes(grid: Grid, N: int, symbols: Sequence[int]) -> bool:
    target = sorted(symbols)
    total_boxes = N * N
    for b in range(total_boxes):
        cells = [grid[r][c] for r, c in box_cells(b, N)]
        if sorted(cells) != sorted(target):
            return False
    return True


def apply_givens(grid: Grid, givens: Grid, mask: Mask) -> Grid:
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            if mask[r][c]:
                row[c] = givens[r][c]
    return grid


def is_valid_individual(grid: Grid, givens: Grid, mask: Mask, N: int, symbols: Sequence[int]) -> bool:
    return check_givens(grid, givens, mask) and check_boxes(grid, N, symbols)
