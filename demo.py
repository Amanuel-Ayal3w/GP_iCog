"""Simple demo script running the Sudoku GES solver on a 9x9 puzzle."""

from __future__ import annotations

from pprint import pprint

from config import Config
from engine import run

PUZZLE = """
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
"""


def main() -> None:
    cfg = Config(
        N=3,
        pop_size=400,
        generations=1000,
        p_cx=0.9,
        p_mut=0.3,
        elite=10,
        tourn_k=4,
        lam=0.05,
        seed=11,
        history_stride=10,
    )
    best, history = run(cfg, PUZZLE)
    print("Best result (conflicts, complexity, fitness):")
    print(best["conflicts"], best["complexity"], best["fitness"])
    print("Grid:")
    for row in best["grid"]:
        print(" ".join(str(cell) for cell in row))
    print("History snapshot:")
    pprint(history[:5])


if __name__ == "__main__":
    main()
