"""Type effectiveness chart (Gen 6+ rules, 18 types, no Fairy-less gens)."""

TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison",
    "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark",
    "Steel", "Fairy",
]

# chart[attacking_type][defending_type] = multiplier
_SUPER = "super"
_NOT = "not"
_IMMUNE = "immune"

_RAW = {
    "Normal":   {"Rock": _NOT, "Ghost": _IMMUNE, "Steel": _NOT},
    "Fire":     {"Fire": _NOT, "Water": _NOT, "Grass": _SUPER, "Ice": _SUPER,
                 "Bug": _SUPER, "Rock": _NOT, "Dragon": _NOT, "Steel": _SUPER},
    "Water":    {"Fire": _SUPER, "Water": _NOT, "Grass": _NOT, "Ground": _SUPER,
                 "Rock": _SUPER, "Dragon": _NOT},
    "Electric": {"Water": _SUPER, "Electric": _NOT, "Grass": _NOT, "Ground": _IMMUNE,
                 "Flying": _SUPER, "Dragon": _NOT},
    "Grass":    {"Fire": _NOT, "Water": _SUPER, "Grass": _NOT, "Poison": _NOT,
                 "Ground": _SUPER, "Flying": _NOT, "Bug": _NOT, "Rock": _SUPER,
                 "Dragon": _NOT, "Steel": _NOT},
    "Ice":      {"Fire": _NOT, "Water": _NOT, "Grass": _SUPER, "Ice": _NOT,
                 "Ground": _SUPER, "Flying": _SUPER, "Dragon": _SUPER, "Steel": _NOT},
    "Fighting": {"Normal": _SUPER, "Ice": _SUPER, "Poison": _NOT, "Flying": _NOT,
                 "Psychic": _NOT, "Bug": _NOT, "Rock": _SUPER, "Ghost": _IMMUNE,
                 "Dark": _SUPER, "Steel": _SUPER, "Fairy": _NOT},
    "Poison":   {"Grass": _SUPER, "Poison": _NOT, "Ground": _NOT, "Rock": _NOT,
                 "Ghost": _NOT, "Steel": _IMMUNE, "Fairy": _SUPER},
    "Ground":   {"Fire": _SUPER, "Electric": _SUPER, "Grass": _NOT, "Poison": _SUPER,
                 "Flying": _IMMUNE, "Bug": _NOT, "Rock": _SUPER, "Steel": _SUPER},
    "Flying":   {"Electric": _NOT, "Grass": _SUPER, "Fighting": _SUPER, "Bug": _SUPER,
                 "Rock": _NOT, "Steel": _NOT},
    "Psychic":  {"Fighting": _SUPER, "Poison": _SUPER, "Psychic": _NOT, "Dark": _IMMUNE,
                 "Steel": _NOT},
    "Bug":      {"Fire": _NOT, "Grass": _SUPER, "Fighting": _NOT, "Poison": _NOT,
                 "Flying": _NOT, "Psychic": _SUPER, "Ghost": _NOT, "Dark": _SUPER,
                 "Steel": _NOT, "Fairy": _NOT},
    "Rock":     {"Fire": _SUPER, "Ice": _SUPER, "Fighting": _NOT, "Ground": _NOT,
                 "Flying": _SUPER, "Bug": _SUPER, "Steel": _NOT},
    "Ghost":    {"Normal": _IMMUNE, "Psychic": _SUPER, "Ghost": _SUPER, "Dark": _NOT},
    "Dragon":   {"Dragon": _SUPER, "Steel": _NOT, "Fairy": _IMMUNE},
    "Dark":     {"Fighting": _NOT, "Psychic": _SUPER, "Ghost": _SUPER, "Dark": _NOT,
                 "Fairy": _NOT},
    "Steel":    {"Fire": _NOT, "Water": _NOT, "Electric": _NOT, "Ice": _SUPER,
                 "Rock": _SUPER, "Steel": _NOT, "Fairy": _SUPER},
    "Fairy":    {"Fire": _NOT, "Fighting": _SUPER, "Poison": _NOT, "Dragon": _SUPER,
                 "Dark": _SUPER, "Steel": _NOT},
}

_MULT = {_SUPER: 2.0, _NOT: 0.5, _IMMUNE: 0.0}


def type_multiplier(attack_type, defender_types):
    """Return the combined multiplier of attack_type against a list of defender types."""
    mult = 1.0
    row = _RAW.get(attack_type, {})
    for dt in defender_types:
        key = row.get(dt)
        mult *= _MULT.get(key, 1.0)
    return mult
