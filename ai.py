"""A lightweight heuristic AI: prefers super-effective / high-damage moves,
switches in a resistant Pokemon if the active one is in bad shape."""

import random

from . import types as type_chart


def score_move(attacker, defender, move):
    if move["category"] == "Status":
        score = 20
        if move.get("status") and defender.status is None:
            score += 15
        if move.get("heal") and attacker.hp_fraction() < 0.5:
            score += 30
        for target, stat, delta in move.get("stat_changes", []):
            if target == "self" and delta > 0:
                score += 10
        return score

    eff = type_chart.type_multiplier(move["type"], defender.types)
    stab = 1.5 if move["type"] in attacker.types else 1.0
    return move["power"] * eff * stab


def choose_action(trainer, opponent):
    mon = trainer.active
    opp = opponent.active

    # consider switching if at low HP and a teammate resists the opponent well
    if mon.hp_fraction() < 0.25 and any(not p.is_fainted for p in trainer.team
                                         if p is not mon):
        alive = [i for i, p in enumerate(trainer.team)
                 if not p.is_fainted and p is not mon]
        best_idx, best_score = None, -999
        for i in alive:
            candidate = trainer.team[i]
            worst_incoming = max(
                (type_chart.type_multiplier(t, candidate.types) for t in opp.types),
                default=1.0,
            )
            score = -worst_incoming
            if score > best_score:
                best_score, best_idx = score, i
        if best_idx is not None and random.random() < 0.5:
            return ("switch", best_idx)

    scored = [(score_move(mon, opp, mv), mv) for mv in mon.moves]
    scored.sort(key=lambda t: t[0], reverse=True)
    # small chance to not pick the very best move, for variety
    top_n = scored[:2] if len(scored) > 1 else scored
    return ("move", random.choice(top_n)[1])
