"""
  Recipes and Achievements
"""
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
    C("water",1,"Container"),
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
    ("salt","sand"):("glass","Fire","Glassware",20),
}

DEFENCES = {
    # nemesis card : need achievement
    "meteor":"Meteor Defense System",
    "plague":"Antibiotics",
    "deforestation":"Land Conservation",
}


