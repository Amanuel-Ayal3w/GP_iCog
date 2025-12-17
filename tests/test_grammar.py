import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from grammar import apply_givens, check_boxes, check_givens, is_valid_individual


def _base_grid() -> list[list[int]]:
    return [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]


def _mask() -> list[list[bool]]:
    return [
        [True, False, False, True],
        [False, False, False, False],
        [False, False, False, False],
        [True, False, False, True],
    ]


class GrammarTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = Config(N=2)
        self.givens = _base_grid()
        self.mask = _mask()

    def test_check_givens_detects_changes(self) -> None:
        grid = [row[:] for row in self.givens]
        grid[0][0] = 9
        print("Givens grid:")
        for row in self.givens:
            print(row)
        print("Modified grid:")
        for row in grid:
            print(row)
        self.assertFalse(check_givens(grid, self.givens, self.mask))

    def test_check_boxes_requires_all_symbols(self) -> None:
        grid = _base_grid()
        grid[0][1] = 1
        self.assertFalse(check_boxes(grid, self.cfg.N, self.cfg.symbols))

    def test_apply_givens_restores_values(self) -> None:
        grid = [row[:] for row in self.givens]
        grid[0][1] = 9
        print("Before apply_givens:")
        for row in grid:
            print(row)
        apply_givens(grid, self.givens, self.mask)
        print("After apply_givens:")
        for row in grid:
            print(row)
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(grid[0][3], 4)

    def test_is_valid_individual_combines_checks(self) -> None:
        grid = _base_grid()
        print("Validation candidate:")
        for row in grid:
            print(row)
        self.assertTrue(is_valid_individual(grid, self.givens, self.mask, self.cfg.N, self.cfg.symbols))


if __name__ == "__main__":
    unittest.main()
