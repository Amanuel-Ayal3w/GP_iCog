import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from puzzle import parse_grid, validate_givens


class PuzzleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = Config(N=2, seed=123)

    def test_parse_grid_from_string(self) -> None:
        data = """
        1 0 0 4
        0 0 0 0
        0 0 0 0
        3 0 0 2
        """
        grid, mask = parse_grid(data, self.cfg.grid_size)
        print("Parsed grid:")
        for row in grid:
            print(row)
        print("Mask row 0:", mask[0])
        self.assertEqual(grid[0][0], 1)
        self.assertEqual(grid[3][3], 2)
        self.assertTrue(mask[0][0])
        self.assertFalse(mask[1][1])

    def test_validate_givens_accepts_symbols(self) -> None:
        puzzle = "1 0 0 4 0 0 0 0 0 0 0 0 3 0 0 2"
        grid, mask = parse_grid(puzzle, self.cfg.grid_size)
        print("Valid givens grid row 0:", grid[0])
        validate_givens(grid, mask, self.cfg.symbols)

    def test_validate_givens_rejects_invalid_symbol(self) -> None:
        grid = [[5, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [3, 0, 0, 2]]
        mask = [
            [True, False, False, True],
            [False, False, False, False],
            [False, False, False, False],
            [True, False, False, True],
        ]
        print("Invalid givens grid row 0:", grid[0])
        with self.assertRaises(ValueError):
            validate_givens(grid, mask, self.cfg.symbols)


if __name__ == "__main__":
    unittest.main()
