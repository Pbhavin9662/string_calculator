# String Calculator (TDD Kata) — Python

## How to run

1. Create a virtual environment and activate it.
2. Install dev deps: `pip install pytest` (or use Poetry / pipenv / tox).
3. From repo root run: `python -m pytest -q`.

## TDD workflow notes (recommended commit steps)

Commit often after each green/red cycle. Example step-by-step commits you can follow:

1. `git init` + initial commit (README).
2. Add failing test for empty string -> implement `add('') -> 0` -> commit.
3. Add test for single number -> implement -> commit.
4. Add test for two numbers -> implement -> commit.
5. Add test for newlines -> implement -> commit.
6. Add test for custom delimiter -> implement header parsing -> commit.
7. Add tests for negative numbers -> implement exception -> commit.
8. Add tests for multi-length and multiple delimiters -> refactor parsing -> commit.
9. Add tests for invalid tokens and None -> make robust -> commit.

Write test-first for every new behavior. After every test passes, do a small refactor and commit.

## Design notes

- Parsing and delimiter handling are separated into small helper methods to keep `add` readable and testable.
- Negative numbers are surfaced via a specific `NegativeNumberError` to make intent explicit in tests and callers.
- Extensive tests cover expected behaviors and edge cases.

## Suggestions for extension (not required by kata)

- Ignore numbers bigger than 1000 (classic optional rule).
- Support multiple delimiter declarations separated by comma in header.
- Add property-based tests using Hypothesis for fuzzing token parsing.
