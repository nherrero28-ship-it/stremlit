"""Turn resolution engine for a 1v1 (single active) battle between two trainers."""

import random

from . import types as type_chart


class Trainer:
    def __init__(self, name, team, is_ai=False):
        self.name = name
        self.team = team  # list[Pokemon]
        self.active_index = 0
        self.is_ai = is_ai
        self.hazards = set()

    @property
    def active(self):
        return self.team[self.active_index]

    def alive_team(self):
        return [p for p in self.team if not p.is_fainted]

    def has_lost(self):
        return len(self.alive_team()) == 0

    def switch_to(self, index):
        self.active_index = index


class Battle:
    def __init__(self, trainer_a, trainer_b, log_fn=print):
        self.a = trainer_a
        self.b = trainer_b
        self.log = log_fn
        self.turn_number = 0

    # ---------- damage math -----------------------------------
    def calc_damage(self, attacker, defender, move):
        if move["category"] == "Status" or move["power"] == 0:
            return 0, 1.0, False
        level = attacker.level
        if move["category"] == "Physical":
            atk = attacker.effective_stat("atk")
            df = defender.effective_stat("def")
        else:
            atk = attacker.effective_stat("spa")
            df = defender.effective_stat("spd")

        base = (((2 * level / 5 + 2) * move["power"] * (atk / max(df, 1))) / 50) + 2

        stab = 1.5 if move["type"] in attacker.types else 1.0
        eff = type_chart.type_multiplier(move["type"], defender.types)
        crit_chance = 1 / 8 if move.get("high_crit") else 1 / 24
        crit = random.random() < crit_chance
        crit_mult = 1.5 if crit else 1.0
        rand = random.uniform(0.85, 1.0)

        dmg = base * stab * eff * crit_mult * rand
        return int(dmg), eff, crit

    def accuracy_check(self, move):
        acc = move.get("accuracy", 100)
        if acc is True or acc is None:
            return True
        return random.uniform(0, 100) <= acc

    # ---------- turn order --------------------------------------
    def _speed(self, trainer):
        return trainer.active.effective_stat("spe")

    def order_actions(self, action_a, action_b):
        """action = ('move', move_dict) or ('switch', index)."""
        a_is_switch = action_a[0] == "switch"
        b_is_switch = action_b[0] == "switch"
        if a_is_switch and not b_is_switch:
            return [("a", action_a), ("b", action_b)]
        if b_is_switch and not a_is_switch:
            return [("b", action_b), ("a", action_a)]
        if a_is_switch and b_is_switch:
            return [("a", action_a), ("b", action_b)]

        prio_a = action_a[1].get("priority", 0)
        prio_b = action_b[1].get("priority", 0)
        if prio_a != prio_b:
            return [("a", action_a), ("b", action_b)] if prio_a > prio_b else \
                   [("b", action_b), ("a", action_a)]

        spe_a, spe_b = self._speed(self.a), self._speed(self.b)
        if spe_a == spe_b:
            first = random.choice(["a", "b"])
            return [(first, action_a if first == "a" else action_b),
                    ("b" if first == "a" else "a", action_b if first == "a" else action_a)]
        return [("a", action_a), ("b", action_b)] if spe_a > spe_b else \
               [("b", action_b), ("a", action_a)]

    # ---------- status / end of turn -----------------------------
    def pre_move_status_block(self, mon):
        """Returns True if mon can act this turn."""
        if mon.status == "slp":
            mon.status_turns -= 1
            if mon.status_turns <= 0:
                mon.status = None
                self.log(f"{mon.name} woke up!")
            else:
                self.log(f"{mon.name} is fast asleep.")
                return False
        if mon.status == "frz":
            if random.random() < 0.2:
                mon.status = None
                self.log(f"{mon.name} thawed out!")
            else:
                self.log(f"{mon.name} is frozen solid!")
                return False
        if mon.status == "par":
            if random.random() < 0.25:
                self.log(f"{mon.name} is paralyzed and can't move!")
                return False
        if mon.confused:
            mon.confuse_turns -= 1
            if mon.confuse_turns <= 0:
                mon.confused = False
                self.log(f"{mon.name} snapped out of confusion.")
            elif random.random() < 0.33:
                self.log(f"{mon.name} is confused and hurt itself!")
                mon.apply_damage(max(1, int(mon.max_hp * 0.1)))
                return False
        if mon.must_recharge:
            mon.must_recharge = False
            self.log(f"{mon.name} must recharge!")
            return False
        return True

    def apply_end_of_turn_status(self, mon):
        if mon.is_fainted:
            return
        if mon.status == "brn":
            dmg = max(1, mon.max_hp // 16)
            mon.apply_damage(dmg)
            self.log(f"{mon.name} is hurt by its burn! (-{dmg} HP)")
        elif mon.status == "psn":
            dmg = max(1, mon.max_hp // 8)
            mon.apply_damage(dmg)
            self.log(f"{mon.name} is hurt by poison! (-{dmg} HP)")
        elif mon.status == "tox":
            dmg = max(1, (mon.max_hp * mon.toxic_counter) // 16)
            mon.apply_damage(dmg)
            mon.toxic_counter += 1
            self.log(f"{mon.name} is badly poisoned! (-{dmg} HP)")

    # ---------- executing a single move --------------------------
    def execute_move(self, attacker_trainer, defender_trainer, move):
        attacker = attacker_trainer.active
        defender = defender_trainer.active

        if attacker.is_fainted:
            return
        if not self.pre_move_status_block(attacker):
            return

        move["pp"] = move.get("pp", 0)
        self.log(f"{attacker.name} used {move['name']}!")

        if not self.accuracy_check(move):
            self.log("But it missed!")
            if move.get("recharge"):
                attacker.must_recharge = True
            return

        if move["category"] in ("Physical", "Special") and move["power"] > 0:
            dmg, eff, crit = self.calc_damage(attacker, defender, move)
            dealt = defender.apply_damage(dmg)
            if eff == 0:
                self.log(f"It doesn't affect {defender.name}...")
            else:
                if eff > 1:
                    self.log("It's super effective!")
                elif eff < 1:
                    self.log("It's not very effective...")
                if crit:
                    self.log("A critical hit!")
                self.log(f"{defender.name} took {dealt} damage. "
                         f"({defender.current_hp}/{defender.max_hp} HP)")
            if move.get("recharge"):
                attacker.must_recharge = True

        # status effect
        if defender.is_fainted:
            pass
        elif move.get("status") and random.uniform(0, 100) < move.get("effect_chance", 100):
            if defender.set_status(move["status"]):
                self.log(f"{defender.name} was afflicted with {move['status'].upper()}!")

        # stat changes
        for target, stat, delta in move.get("stat_changes", []):
            chance = move.get("effect_chance", 100) if move["category"] != "Status" else 100
            if random.uniform(0, 100) >= chance:
                continue
            mon = attacker if target == "self" else defender
            if mon.is_fainted:
                continue
            actual = mon.change_stage(stat, delta)
            if actual == 0:
                self.log(f"{mon.name}'s {stat} won't go any higher/lower!")
            else:
                direction = "rose" if actual > 0 else "fell"
                self.log(f"{mon.name}'s {stat} {direction}!")

        if move.get("heal"):
            healed = attacker.heal(int(attacker.max_hp * move["heal"]))
            self.log(f"{attacker.name} recovered {healed} HP!")

        if defender.is_fainted:
            self.log(f"{defender.name} fainted!")

    # ---------- public turn API -----------------------------------
    def run_turn(self, action_a, action_b):
        """action = ('move', move_dict) | ('switch', index)"""
        self.turn_number += 1
        self.log(f"\n--- Turn {self.turn_number} ---")

        order = self.order_actions(action_a, action_b)
        for side, action in order:
            trainer = self.a if side == "a" else self.b
            other = self.b if side == "a" else self.a

            if trainer.active.is_fainted:
                continue

            if action[0] == "switch":
                trainer.switch_to(action[1])
                self.log(f"{trainer.name} sent out {trainer.active.name}!")
                continue

            if other.active.is_fainted:
                # opponent already fainted this turn, nothing to hit
                continue

            self.execute_move(trainer, other, action[1])

            if self.a.has_lost() or self.b.has_lost():
                break

        for trainer in (self.a, self.b):
            mon = trainer.active
            if not mon.is_fainted:
                self.apply_end_of_turn_status(mon)

        if self.a.has_lost():
            self.log(f"\n{self.a.name} has no Pokemon left! {self.b.name} wins!")
        elif self.b.has_lost():
            self.log(f"\n{self.b.name} has no Pokemon left! {self.a.name} wins!")

    def winner(self):
        if self.a.has_lost():
            return self.b
        if self.b.has_lost():
            return self.a
        return None
