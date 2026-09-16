# PyMon Battle — Offline Showdown-Style Battle Simulator

A fully offline, terminal-based Pokémon battle simulator written in pure
Python (standard library only, no dependencies). Inspired by the battle
mechanics of Pokémon Showdown: type effectiveness, stat stages, status
conditions, priority/speed-based turn order, critical hits, and a simple
heuristic AI opponent.

> Note: This project uses an original, fan-made "dex" (renamed
> creatures/moves inspired by classic archetypes) instead of Nintendo/Game
> Freak's trademarked names and data, so it's safe to publish and reuse
> freely. Swap in your own names/movepools in `pkmnbattle/species.py` if
> you want to reskin it for personal use.

## Features

- 18-type effectiveness chart (dual-type stacking included)
- Gen-style damage formula (level, STAB, crit, random spread, type multiplier)
- Status conditions: burn, paralysis, poison, toxic (badly poisoned), sleep, freeze
- Stat stage changes (±6 stages, standard multiplier table)
- Priority moves and speed-based turn ordering (with speed ties)
- Switching, fainting, and forced switch-in
- A basic heuristic AI: picks strong/super-effective moves and switches
  out of bad matchups
- Random or manual team building (3v3, easily extended to 6v6)
- Unit tests (`test_battle.py`) verifying the type chart and full
  AI-vs-AI battles

## Getting Started

No dependencies to install — just Python 3.8+.

```bash
python main.py
```

Follow the prompts to build your team (random or hand-picked) and battle
the AI opponent turn by turn.

## Running Tests

```bash
python -m unittest test_battle.py -v
```

## Project Structure

```
.
├── main.py                # CLI entry point / game loop
├── pkmnbattle/
│   ├── battle.py           # Turn resolution engine, damage formula
│   ├── ai.py                # Opponent decision-making
│   ├── pokemon.py           # Battle-ready Pokemon instance (stats, status)
│   ├── species.py           # Species base stats / types / movepools
│   ├── moves.py             # Move database
│   ├── team.py               # Team-building helpers
│   └── types.py               # Type effectiveness chart
└── test_battle.py           # Sanity / regression tests
```

## Extending It

- **Add more species**: add an entry to `SPECIES` in `pkmnbattle/species.py`
  with base stats `(HP, Atk, Def, SpA, SpD, Spe)`, types, and a movepool.
- **Add more moves**: add an entry to `MOVES` in `pkmnbattle/moves.py`.
- **6v6 battles**: change `size=3` to `size=6` in `main.py`'s `pick_team()`
  and `random_team()` calls.
- **Smarter AI**: `pkmnbattle/ai.py` is intentionally simple — a good spot
  to add minimax/expectimax lookahead or damage-roll simulation.

## License

MIT — see `LICENSE`.
