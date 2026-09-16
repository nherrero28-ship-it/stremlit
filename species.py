"""Species database: base stats, types, and learnable movepool.

Base stats order: HP, Atk, Def, SpA, SpD, Spe
Names are original/renamed to avoid reproducing trademarked character names
1:1 in a public repo, while keeping the flavor of classic starter-style
archetypes. Feel free to rename back to your own fan-dex.
"""

SPECIES = {
    "Emberwyrm": dict(types=["Fire"], base=(60, 68, 55, 90, 58, 80),
                       pool=["Ember", "Flamethrower", "Fire Blast", "Quick Attack",
                             "Dragon Claw", "Swords Dance"]),
    "Aquafin":   dict(types=["Water"], base=(74, 65, 70, 85, 80, 62),
                       pool=["Water Gun", "Surf", "Hydro Pump", "Ice Beam",
                             "Recover", "Bite"]),
    "Vinewhip":  dict(types=["Grass", "Poison"], base=(80, 75, 75, 85, 90, 55),
                       pool=["Vine Whip", "Razor Leaf", "Solar Beam", "Sludge Bomb",
                             "Toxic", "Growl"]),
    "Voltmouse": dict(types=["Electric"], base=(55, 55, 40, 65, 55, 105),
                       pool=["Thunder Shock", "Thunderbolt", "Thunder", "Quick Attack",
                             "Agility", "Iron Tail"]),
    "Gustavian": dict(types=["Flying", "Normal"], base=(63, 60, 55, 50, 50, 71),
                       pool=["Gust", "Wing Attack", "Air Slash", "Quick Attack",
                             "Body Slam", "Growl"]),
    "Brawlrilla":dict(types=["Fighting"], base=(80, 100, 70, 50, 60, 45),
                       pool=["Close Combat", "Karate Chop", "Rock Slide", "Bite",
                             "Swords Dance", "Iron Head"]),
    "Duskraven": dict(types=["Ghost", "Dark"], base=(60, 65, 60, 85, 65, 95),
                       pool=["Shadow Ball", "Lick", "Crunch", "Confusion",
                             "Psychic", "Toxic"]),
    "Terraquake":dict(types=["Ground", "Rock"], base=(100, 90, 100, 60, 60, 45),
                       pool=["Earthquake", "Dig", "Rock Slide", "Iron Tail",
                             "Body Slam", "Stealth Rock"]),
    "Glacielle": dict(types=["Ice", "Fairy"], base=(70, 55, 65, 95, 95, 65),
                       pool=["Ice Beam", "Blizzard", "Moonblast", "Dazzling Gleam",
                             "Recover", "Thunder Wave"]),
    "Steelclaw": dict(types=["Steel"], base=(65, 95, 110, 45, 60, 50),
                       pool=["Iron Head", "Iron Tail", "Rock Slide", "Crunch",
                             "Swords Dance", "Body Slam"]),
    "Buzzscythe":dict(types=["Bug", "Flying"], base=(65, 90, 55, 60, 55, 90),
                       pool=["X-Scissor", "Bug Bite", "Air Slash", "Quick Attack",
                             "Swords Dance", "Wing Attack"]),
    "Drakonyx":  dict(types=["Dragon"], base=(91, 100, 80, 100, 80, 95),
                       pool=["Dragon Claw", "Dragon Breath", "Hyper Beam",
                             "Fire Blast", "Ice Beam", "Agility"]),
    "Psymajesty":dict(types=["Psychic"], base=(70, 55, 65, 105, 95, 90),
                       pool=["Psychic", "Confusion", "Shadow Ball", "Ice Beam",
                             "Recover", "Thunder Wave"]),
    "Toxiquill": dict(types=["Poison", "Dark"], base=(70, 85, 65, 55, 65, 85),
                       pool=["Sludge Bomb", "Poison Sting", "Crunch", "Bite",
                             "Toxic", "Swords Dance"]),
    "Normanteau":dict(types=["Normal"], base=(95, 80, 70, 60, 65, 75),
                       pool=["Tackle", "Body Slam", "Hyper Beam", "Quick Attack",
                             "Iron Tail", "Growl"]),
    "Faerivel":  dict(types=["Fairy"], base=(75, 60, 70, 95, 100, 70),
                       pool=["Moonblast", "Dazzling Gleam", "Psychic", "Ice Beam",
                             "Recover", "Thunder Wave"]),
}


def get_species(name):
    return SPECIES[name]


def list_species():
    return list(SPECIES.keys())
