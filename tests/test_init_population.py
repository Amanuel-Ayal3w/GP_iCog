import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from grammar import is_valid_individual
from init_population import init_individual, init_population
from puzzle import parse_grid


class InitPopulationTests(unittest.TestCase):
    def _givens(self) -> tuple[list[list[int]], list[list[bool]], Config]:
        cfg = Config(N=2, seed=321)
        givens, mask = parse_grid("1 0 0 4 0 0 0 0 0 0 0 0 3 0 0 2", cfg.grid_size)
        return givens, mask, cfg

    def test_init_individual_respects_grammar(self) -> None:
        givens, mask, cfg = self._givens()
        ind = init_individual(givens, mask, cfg, random.Random(cfg.seed))
        print("Initialized individual grid:")
        for row in ind.grid:
            print(row)
        self.assertTrue(is_valid_individual(ind.grid, givens, mask, cfg.N, cfg.symbols))

    def test_init_population_size(self) -> None:
        givens, mask, cfg = self._givens()
        cfg.pop_size = 10
        pop = init_population(cfg, givens, mask)
        print("Population size:", len(pop))
        print("First individual grid:")
        for row in pop[0].grid:
            print(row)
        self.assertEqual(len(pop), cfg.pop_size)
        for ind in pop:
            self.assertTrue(is_valid_individual(ind.grid, givens, mask, cfg.N, cfg.symbols))


if __name__ == "__main__":
    unittest.main()
