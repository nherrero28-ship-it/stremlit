import random

from . import species as species_db
from .pokemon import Pokemon


def random_team(size=3, level=50):
    names = random.sample(species_db.list_species(), k=size)
    return [Pokemon(n, level=level) for n in names]


def build_team(names, level=50):
    return [Pokemon(n, level=level) for n in names]
