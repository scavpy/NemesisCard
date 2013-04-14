"""
  Recipes and Achievements
"""
from collections import namedtuple

C = namedtuple("C","name rarity need")

VEGETABLES = [
    C("stick",1,None),
    C("twigs",1,None),
    C("grass",1,None),
    ]

ANIMALS = [
    C("skin",1,None),
    C("ivory",10,"Hunting"),
    ]

MINERALS = [
    C("dirt",1,None),
    C("water",1,"Container"),
    C("clay",2,None),
    C("flint",5,None),
    ]

STOCK = {"animals":ANIMALS,
         "vegetables":VEGETABLES,
         "minerals":MINERALS}

RECIPES = {
    # ingedients : (get card, need achievement, get achievement, score)
    ("flint","stick"):("spear",None,"Hunting",5),
}

DEFENCES = {
    # nemesis card : need achievement
    "meteor":"Meteor Defense System",
    "plague":"Antibiotics",
    "deforestation":"Land Conservation",
}


