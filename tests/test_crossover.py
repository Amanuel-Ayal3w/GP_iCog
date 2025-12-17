import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from grammar import check_boxes, check_givens
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
        self.assertTrue(check_givens(child1.grid, givens, mask))
        self.assertTrue(check_givens(child2.grid, givens, mask))
        self.assertTrue(check_boxes(child1.grid, cfg.N, cfg.symbols))
        self.assertTrue(check_boxes(child2.grid, cfg.N, cfg.symbols))
        self.assertLessEqual(child1.complexity, parent1.complexity)
        self.assertLessEqual(child2.complexity, parent2.complexity)


if __name__ == "__main__":
    unittest.main()
