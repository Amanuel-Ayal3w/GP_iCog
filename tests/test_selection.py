import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from individual import Individual
from ops.selection import tournament


class SelectionTests(unittest.TestCase):
    def test_tournament_prefers_lower_complexity(self) -> None:
        cfg = Config(N=2, tourn_k=4)
        grid = [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
        individuals = [
            Individual([row[:] for row in grid], conflicts=1, complexity=3, fitness=-4.0),
            Individual([row[:] for row in grid], conflicts=1, complexity=1, fitness=-2.0),
            Individual([row[:] for row in grid], conflicts=2, complexity=0, fitness=-2.0),
            Individual([row[:] for row in grid], conflicts=1, complexity=2, fitness=-3.0),
        ]
        rng = random.Random(0)
        winner = tournament(individuals, cfg, rng)
        self.assertEqual(winner.complexity, 1)


if __name__ == "__main__":
    unittest.main()
