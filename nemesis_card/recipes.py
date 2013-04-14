"""
  Recipes and Achievements
"""
from collections import namedtuple

C = namedtuple("C","name rarity need")

VEGETABLES = [
    C("stick",1,None),
    C("twigs",1,None),
    C("grass",1,None),
    C("deforestation",50,"Nemesis"),
    ]

ANIMALS = [
    C("skin",1,None),
    C("ivory",10,"Hunting"),
    C("plague",200,"Nemesis"),
    ]

MINERALS = [
    C("dirt",1,None),
    C("water",1,"Container"),
    C("clay",2,None),
    C("flint",5,None),
    C("sand",2,None),
    C("salt",5,None),
    C("meteor",500,"Nemesis"),
    C("balrog",400,"Nemesis"),
    ]

STOCK = {"animals":ANIMALS,
         "vegetables":VEGETABLES,
         "minerals":MINERALS}

RECIPES = {
    # ingedients : (get card, need achievement, get achievement, score)
    ("flint","stick"):("spear",None,"Hunting",5),
    ("flint","twigs"):("ash",None,"Fire",10),
    ("salt","sand"):("glass","Fire","Glassware",20),
}

DEFENCES = {
    # nemesis card : need achievement
    "meteor":"Meteor Defense System",
    "plague":"Antibiotics",
    "deforestation":"Land Conservation",
}


