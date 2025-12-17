import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from grammar import check_boxes, check_givens
from individual import Individual
from ops.mutation import mut_swap_in_box


class MutationTests(unittest.TestCase):
    def test_mutation_preserves_constraints(self) -> None:
        cfg = Config(N=2, seed=5)
        givens = [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 1, 4, 3],
            [4, 3, 2, 1],
        ]
        mask = [[False] * cfg.grid_size for _ in range(cfg.grid_size)]
        ind = Individual([row[:] for row in givens])
        rng = random.Random(123)
        child = mut_swap_in_box(ind, cfg, givens, mask, rng)
        print("Mutation input:")
        for row in ind.grid:
            print(row)
        print("Mutation output:")
        for row in child.grid:
            print(row)
        self.assertTrue(check_givens(child.grid, givens, mask))
        self.assertTrue(check_boxes(child.grid, cfg.N, cfg.symbols))
        self.assertGreaterEqual(child.complexity, ind.complexity)


if __name__ == "__main__":
    unittest.main()
