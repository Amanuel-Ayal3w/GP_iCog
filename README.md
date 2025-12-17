# Grammar-Guided Sudoku Solver

## Overview

This project implements a grammar-guided evolutionary search (GES) solver for Sudoku puzzles. Every candidate grid respects Sudoku box and given-cell constraints by construction, while the evolutionary loop drives the population toward solutions using conflict minimization and a complexity penalty.

## Project Layout

- config.py — searchable parameters shared across the solver
- puzzle.py — parsing helpers for Sudoku grids
- grammar.py — grammar-style validity checks and repairs
- individual.py — data structure representing a candidate grid
- init_population.py — grammar-respecting population initialization
- fitness.py — conflict scoring with complexity penalties
- ops/ — selection, crossover, mutation, and replacement operators
- engine.py — evolutionary search loop orchestrator
- reporting.py — utilities to persist run summaries
- demo.py — sample script that runs the solver on a 9×9 puzzle
- tests/ — unittest-based coverage for core modules

## Requirements

- Python 3.10 or newer
- (Optional) Virtual environment for isolation

To create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## Running the Solver Demo

Execute the included 9×9 example via the demo script:

```bash
python3 demo.py
```

The script prints the best grid found, its conflict count, complexity, fitness, and a snapshot of historical progress.

## Running Tests

All tests (recommended before commits):

```bash
python3 -m unittest discover -s tests
```

Single test module (for faster iteration):

```bash
python3 -m unittest tests.test_engine
```

Single test case (deep dive on one scenario):

```bash
python3 -m unittest tests.test_engine.EngineTests.test_engine_respects_seed_and_returns_solution
```

## Reproducibility Tips

- Adjust configuration values directly in config.py or when instantiating Config.
- Set `Config.seed` to control stochastic operators for repeatable runs.
- Increase `generations` or `pop_size` to search longer or broaden the population when tackling difficult puzzles.