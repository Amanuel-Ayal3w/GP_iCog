import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from fitness import conflicts, score
from individual import Individual


def _solved_grid() -> list[list[int]]:
    return [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]


class FitnessTests(unittest.TestCase):
    def test_conflicts_zero_for_solved(self) -> None:
        cfg = Config(N=2)
        self.assertEqual(conflicts(_solved_grid(), cfg), 0)

    def test_score_penalizes_complexity(self) -> None:
        cfg = Config(N=2, lam=1.0)
        ind_base = Individual(_solved_grid(), complexity=0)
        ind_penalized = Individual(_solved_grid(), complexity=3)
        score(ind_base, cfg)
        score(ind_penalized, cfg)
        self.assertGreater(ind_base.fitness, ind_penalized.fitness)


if __name__ == "__main__":
    unittest.main()
