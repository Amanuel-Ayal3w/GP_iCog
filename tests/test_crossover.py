import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from grammar import check_boxes, check_givens


def _has_contribution(child: list[list[int]], primary: list[list[int]], secondary: list[list[int]]) -> bool:
    seen_primary = False
    seen_secondary = False
    for r, row in enumerate(child):
        for c, value in enumerate(row):
            if primary[r][c] != secondary[r][c]:
                if value == primary[r][c]:
                    seen_primary = True
                if value == secondary[r][c]:
                    seen_secondary = True
            else:
                if value == primary[r][c]:
                    seen_primary = True
                    seen_secondary = True
        if seen_primary and seen_secondary:
            return True
    return seen_primary and seen_secondary
from individual import Individual
from ops.crossover import cx_boxes


class CrossoverTests(unittest.TestCase):
    def test_crossover_preserves_boxes_and_givens(self) -> None:
        cfg = Config(N=2)
        givens = [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 1, 4, 3],
            [4, 3, 2, 1],
        ]
        mask = [[False] * cfg.grid_size for _ in range(cfg.grid_size)]
        parent1 = Individual([row[:] for row in givens], complexity=2)
        parent2 = Individual([row[::-1] for row in givens], complexity=5)
        rng = random.Random(99)
        child1, child2 = cx_boxes(parent1, parent2, cfg, givens, mask, rng)
        print("Parent 1:")
        for row in parent1.grid:
            print(row)
        print("Parent 2:")
        for row in parent2.grid:
            print(row)
        print("Child 1:")
        for row in child1.grid:
            print(row)
        print("Child 2:")
        for row in child2.grid:
            print(row)
        self.assertNotEqual(child1.grid, parent1.grid)
        self.assertNotEqual(child1.grid, parent2.grid)
        self.assertNotEqual(child2.grid, parent1.grid)
        self.assertNotEqual(child2.grid, parent2.grid)
        self.assertTrue(
            _has_contribution(child1.grid, parent1.grid, parent2.grid),
            "child1 should include cells from both parents",
        )
        self.assertTrue(
            _has_contribution(child2.grid, parent2.grid, parent1.grid),
            "child2 should include cells from both parents",
        )
        self.assertTrue(check_givens(child1.grid, givens, mask))
        self.assertTrue(check_givens(child2.grid, givens, mask))
        self.assertTrue(check_boxes(child1.grid, cfg.N, cfg.symbols))
        self.assertTrue(check_boxes(child2.grid, cfg.N, cfg.symbols))
        self.assertGreaterEqual(child1.complexity, min(parent1.complexity, parent2.complexity))
        self.assertLessEqual(child1.complexity, max(parent1.complexity, parent2.complexity))
        self.assertGreaterEqual(child2.complexity, min(parent1.complexity, parent2.complexity))
        self.assertLessEqual(child2.complexity, max(parent1.complexity, parent2.complexity))


if __name__ == "__main__":
    unittest.main()
