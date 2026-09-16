"""A single battle-ready Pokemon instance."""

import random

from . import species as species_db
from . import moves as moves_db

STAT_NAMES = ["hp", "atk", "def", "spa", "spd", "spe"]


def calc_stat(base, level, is_hp, iv=31, ev=0):
    if is_hp:
        return int(((2 * base + iv + ev // 4) * level) / 100) + level + 10
    return int((((2 * base + iv + ev // 4) * level) / 100) + 5)


class Pokemon:
    def __init__(self, name, level=50, moves=None):
        data = species_db.get_species(name)
        self.name = name
        self.types = list(data["types"])
        self.level = level
        base = data["base"]
        self.base_stats = dict(zip(STAT_NAMES, base))

        self.stats = {}
        for i, stat in enumerate(STAT_NAMES):
            self.stats[stat] = calc_stat(base[i], level, is_hp=(stat == "hp"))

        self.max_hp = self.stats["hp"]
        self.current_hp = self.max_hp

        pool = data["pool"]
        chosen = moves or random.sample(pool, k=min(4, len(pool)))
        self.moves = [moves_db.get_move(m) for m in chosen]

        self.status = None       # 'brn','par','psn','tox','slp','frz'
        self.status_turns = 0
        self.toxic_counter = 1
        self.stat_stages = {s: 0 for s in ["atk", "def", "spa", "spd", "spe"]}
        self.must_recharge = False
        self.confused = False
        self.confuse_turns = 0

    # -- helpers -------------------------------------------------
    @property
    def is_fainted(self):
        return self.current_hp <= 0

    def stage_multiplier(self, stage):
        stage = max(-6, min(6, stage))
        if stage >= 0:
            return (2 + stage) / 2
        return 2 / (2 - stage)

    def effective_stat(self, stat):
        val = self.stats[stat] * self.stage_multiplier(self.stat_stages.get(stat, 0))
        if stat == "atk" and self.status == "brn":
            val *= 0.5
        if stat == "spe" and self.status == "par":
            val *= 0.5
        return val

    def apply_damage(self, dmg):
        dmg = max(0, min(self.current_hp, dmg))
        self.current_hp -= dmg
        return dmg

    def heal(self, amount):
        healed = min(self.max_hp - self.current_hp, amount)
        self.current_hp += healed
        return healed

    def change_stage(self, stat, delta):
        old = self.stat_stages[stat]
        new = max(-6, min(6, old + delta))
        self.stat_stages[stat] = new
        return new - old

    def set_status(self, status):
        if self.status is not None:
            return False
        # simple type immunities
        if status == "brn" and "Fire" in self.types:
            return False
        if status in ("par",) and "Electric" in self.types:
            return False
        if status in ("psn", "tox") and ("Poison" in self.types or "Steel" in self.types):
            return False
        if status == "frz" and "Ice" in self.types:
            return False
        self.status = status
        self.toxic_counter = 1
        if status == "slp":
            self.status_turns = random.randint(1, 3)
        return True

    def hp_fraction(self):
        return self.current_hp / self.max_hp if self.max_hp else 0

    def __str__(self):
        return f"{self.name} Lv.{self.level} ({self.current_hp}/{self.max_hp} HP)"
