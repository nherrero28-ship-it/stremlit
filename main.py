#!/usr/bin/env python3
"""Offline terminal Pokemon battle simulator.

Run:  python main.py
"""

import random
import sys

from pkmnbattle import species as species_db
from pkmnbattle.pokemon import Pokemon
from pkmnbattle.battle import Battle, Trainer
from pkmnbattle import ai as ai_module
from pkmnbattle.team import random_team, build_team

BANNER = r"""
  ____       _              __  __             ____        _   _   _
 |  _ \ ___ | | _____ _ __ |  \/  | ___  _ __  | __ )  __ _| |_| |_| | ___
 | |_) / _ \| |/ / _ \ '_ \| |\/| |/ _ \| '_ \ |  _ \ / _` | __| __| |/ _ \
 |  __/ (_) |   <  __/ | | | |  | | (_) | | | || |_) | (_| | |_| |_| |  __/
 |_|   \___/|_|\_\___|_| |_|_|  |_|\___/|_| |_||____/ \__,_|\__|\__|_|\___|
              (offline Showdown-style battle sim, pure Python)
"""


def prompt_choice(prompt, options):
    while True:
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print("Invalid choice, try again.\n")


def pick_team():
    print("\nHow would you like to build your team?")
    idx = prompt_choice("", ["Random team (3 Pokemon)", "Pick my own team (3 Pokemon)"])
    if idx == 0:
        return random_team(size=3)
    all_species = species_db.list_species()
    chosen = []
    remaining = list(all_species)
    for slot in range(3):
        i = prompt_choice(f"\nChoose Pokemon #{slot + 1}:", remaining)
        chosen.append(remaining.pop(i))
    return build_team(chosen)


def describe_team(team):
    for p in team:
        types = "/".join(p.types)
        move_names = ", ".join(m["name"] for m in p.moves)
        print(f"  - {p.name} ({types})  HP {p.max_hp}  moves: {move_names}")


def player_turn(trainer, opponent):
    mon = trainer.active
    print(f"\nWhat will {mon.name} do?")
    options = [f"{m['name']} ({m['type']}, {m['category']}, pow {m['power']})"
               for m in mon.moves]
    can_switch = any(not p.is_fainted and p is not mon for p in trainer.team)
    if can_switch:
        options.append("Switch Pokemon")
    idx = prompt_choice("", options)
    if can_switch and idx == len(options) - 1:
        alive = [i for i, p in enumerate(trainer.team)
                 if not p.is_fainted and p is not mon]
        names = [trainer.team[i].name for i in alive]
        sub = prompt_choice("Switch to:", names)
        return ("switch", alive[sub])
    return ("move", mon.moves[idx])


def forced_switch(trainer):
    alive = [i for i, p in enumerate(trainer.team) if not p.is_fainted]
    if len(alive) == 1:
        return alive[0]
    names = [trainer.team[i].name for i in alive]
    idx = prompt_choice(f"\n{trainer.name}, choose your next Pokemon:", names)
    return alive[idx]


def main():
    random.seed()
    print(BANNER)
    print("Welcome, trainer! Build your squad and battle an AI opponent.\n")

    player_team = pick_team()
    print("\nYour team:")
    describe_team(player_team)

    ai_team = random_team(size=3)
    print("\nOpponent's team (hidden species revealed on send-out)...")

    player = Trainer("You", player_team)
    opponent = Trainer("Rival AI", ai_team, is_ai=True)

    print(f"\n{player.name} sends out {player.active.name}!")
    print(f"{opponent.name} sends out {opponent.active.name}!")

    battle = Battle(player, opponent, log_fn=print)

    while not player.has_lost() and not opponent.has_lost():
        if player.active.is_fainted:
            player.switch_to(forced_switch(player))
            print(f"Go, {player.active.name}!")
            continue
        if opponent.active.is_fainted:
            opponent.switch_to(forced_switch(opponent))
            print(f"{opponent.name} sends out {opponent.active.name}!")
            continue

        p_action = player_turn(player, opponent)
        o_action = ai_module.choose_action(opponent, player)
        battle.run_turn(p_action, o_action)

    winner = battle.winner()
    print(f"\n=== {winner.name} wins the battle! ===")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBattle interrupted. Goodbye!")
        sys.exit(0)
