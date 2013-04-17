"""
  Recipes and Achievements
"""
import logging
from collections import namedtuple

C = namedtuple("C","name rarity need")

VEGETABLES = [
    C("stick",1,None),
    C("twigs",1,None),
    C("grass",1,None),
    C("deforestation",1,"Nemesis"),
    ]

ANIMALS = [
    C("skin",1,"Hunting"),
    C("ivory",1,"Hunting"),
    C("plague",1,"Nemesis"),
    ]

MINERALS = [
    C("dirt",1,None),
    C("water",1,"Containers"),
    C("clay",1,None),
    C("flint",1,None),
    C("sand",1,None),
    C("salt",1,None),
    C("meteor",1,"Nemesis"),
    C("balrog",1,"Nemesis"),
    ]

STOCK = {"animals":ANIMALS,
         "vegetables":VEGETABLES,
         "minerals":MINERALS}

RECIPES = {
    # ingedients : (get card, need achievement, get achievement, score)
    ("flint","stick"):("spear",None,"Hunting",5),
    ("flint","twigs"):("ash",None,"Fire",10),
    ("flint","grass"):("ash",None,"Fire",10),
    ("grass","grass"):("string",None,None,0),
    ("salt","skin"):("leather",None,None,0),
    ("leather","string"):("bag",None,"Containers",10),
    ("salt","sand"):("glass","Fire","Glassware",20),
}

NEMESES = {
    # nemesis card : (defence, description)
    "meteor":("Meteor Defense System", "a huge meteor."),
    "balrog":("Fire Engines", "a terrible Balrog. You dug too deep and awoke shadow and flame."),
    "plague":("Antibiotics", "a horrific plague."),
    "deforestation":("Land Conservation", "reckless deforestation."),
}


def check_cards():
    """ return a list of cardname, problems
    where problems is space-separated set maybe containing:
       unavailable - for cards that can never be obtained
       nocounter - for nemesis cards whose countering tech can never be obtained
    """
    resource_cards = ANIMALS + VEGETABLES + MINERALS
    known_cards = set(c.name for c in resource_cards)
    reachable_cards = set()
    possible_tech = set([None])
    nemeses = set(c.name for c in resource_cards if c.need == "Nemesis")

    # nemesis cards and ordinary resources are definitely available
    for c in resource_cards:
        if c.need in (None, "Nemesis"):
            reachable_cards.add(c.name)
    # mutually-recursive card and tech searching functions, memoed in reachable_cards and possible_tech
    def can_gain_tech(aname):
        """ can gain tech if it's in a recipe and cards are available """
        if aname in possible_tech:
            return True
        for (c1, c2), (c3, need, gain, pts) in RECIPES.items():
            if gain == aname and can_gain_card(c1) and can_gain_card(c2) and can_gain_tech(need):
                possible_tech.add(aname)
                reachable_cards.add(c3)
                known_cards.update([c1, c2, c3])
                return True
        logging.warning("cannot gain {0}".format(aname))
        return False
    
    def can_gain_card(cname):
        """ can gain card if craftable or obtainable in card decks """
        if cname in reachable_cards:
            return True
        for c in resource_cards:
            if cname == c.name and can_gain_tech(c.need):
                reachable_cards.add(cname)
                return True
        for (c1, c2), (c3, need, gain, pts) in RECIPES.items():
            if c3 == cname and can_gain_card(c1) and can_gain_card(c2) and can_gain_tech(need):
                possible_tech.add(gain)
                reachable_cards.add(c3)
                known_cards.update([c1,c2])
                return True
        return False
        logging.warning("cannot gain {0}".format(cname))

    known_cards |= set(r[0] for r in RECIPES.values())
    for ingredients in RECIPES:
        known_cards |= set(ingredients)

    for cname, (need, desc) in NEMESES.items():
        if can_gain_tech(need):
            try:
                nemeses.remove(cname)
            except KeyError:
                known_cards.add(cname)
    # examine cards known but obviously not needed for countering nemeses
    for c in known_cards - reachable_cards:
        can_gain_card(c)

    cardlist = []
    for c in sorted(known_cards):
        problems = set()
        if c not in reachable_cards:
            problems.add("unavailable")
        if c in nemeses:
            problems.add("nocounter")
        cardlist.append((c, " ".join(problems)))
    return cardlist

