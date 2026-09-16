"""Quick sanity tests. Run with: python -m unittest test_battle.py"""

import random
import unittest

from pkmnbattle.team import random_team
from pkmnbattle.battle import Battle, Trainer
from pkmnbattle import ai as ai_module
from pkmnbattle import types as type_chart


class TestTypeChart(unittest.TestCase):
    def test_super_effective(self):
        self.assertEqual(type_chart.type_multiplier("Water", ["Fire"]), 2.0)

    def test_immune(self):
        self.assertEqual(type_chart.type_multiplier("Normal", ["Ghost"]), 0.0)

    def test_dual_type_stack(self):
        # Water vs Fire/Rock: super x super = 4x
        self.assertEqual(type_chart.type_multiplier("Water", ["Fire", "Rock"]), 4.0)


class TestBattleSimulation(unittest.TestCase):
    def run_ai_battle(self, seed):
        random.seed(seed)
        a = Trainer("A", random_team(3))
        b = Trainer("B", random_team(3))
        battle = Battle(a, b, log_fn=lambda *args, **kwargs: None)

        turns = 0
        while not a.has_lost() and not b.has_lost() and turns < 300:
            if a.active.is_fainted:
                a.switch_to(next(i for i, p in enumerate(a.team) if not p.is_fainted))
                turns += 1
                continue
            if b.active.is_fainted:
                b.switch_to(next(i for i, p in enumerate(b.team) if not p.is_fainted))
                turns += 1
                continue
            battle.run_turn(ai_module.choose_action(a, b), ai_module.choose_action(b, a))
            turns += 1
        return battle, turns

    def test_battles_terminate_with_a_winner(self):
        for seed in range(10):
            battle, turns = self.run_ai_battle(seed)
            self.assertLess(turns, 300, "battle did not terminate")
            self.assertIsNotNone(battle.winner())


if __name__ == "__main__":
    unittest.main()
