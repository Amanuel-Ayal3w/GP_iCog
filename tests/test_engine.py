import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Config
from engine import run


class EngineTests(unittest.TestCase):
    def test_engine_respects_seed_and_returns_solution(self) -> None:
        cfg = Config(N=2, pop_size=5, generations=5, seed=7)
        solved = """
        1 2 3 4
        3 4 1 2
        2 1 4 3
        4 3 2 1
        """
        best, history = run(cfg, solved)
        self.assertEqual(best["conflicts"], 0)
        self.assertEqual(best["complexity"], 0)
        self.assertEqual(history[0]["generation"], 0)
        self.assertEqual(history[0]["best_conflicts"], 0)


if __name__ == "__main__":
    unittest.main()
