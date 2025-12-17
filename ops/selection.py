"""Selection operators."""

from __future__ import annotations

import random
from typing import List

from config import Config
from fitness import better
from individual import Individual


def tournament(population: List[Individual], cfg: Config, rng: random.Random) -> Individual:
    if len(population) < cfg.tourn_k:
        raise ValueError("population too small for tournament")
    contenders = rng.sample(population, cfg.tourn_k)
    winner = contenders[0]
    for challenger in contenders[1:]:
        if better(challenger, winner):
            winner = challenger
    return winner
