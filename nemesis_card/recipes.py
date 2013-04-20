"""
  Recipes and Achievements
"""
import logging
from collections import namedtuple

C = namedtuple("C","name rarity need")

VEGETABLES = [
    C("stick",1,None),
    C("twigs",2,None),
    C("grass",1,None),
    C("log",2,None),
    C("wheat",2,"Agriculture"),
#    C("latex",2,None),
    C("deforestation",80,"Nemesis"),
    C("winter",20,"Nemesis"),
    C("oil",10,"Containers"),
    ]

ANIMALS = [
    C("skin",1,"Hunting"),
#    C("ivory",1,"Hunting"),
    C("bone",3,None),
    C("chicken",10,None),
    C("plague",100,"Nemesis"),
 #   C("snake",1,None),
    C("meat",10,"Hunting"),
    C("blood",20,"Containers"),
    C("DNA",10,"Microbiology"),
    C("winter",50,"Nemesis"),
    ]

MINERALS = [
    C("dirt",3,None),
    C("water",2,"Containers"),
    C("clay",5,None),
    C("flint",2,None),
    C("sand",2,None),
    C("salt",2,None),
    C("copper",3,None),
    C("ironore",3,"Bronze Tools"),
    C("coal",2,"Bronze Tools"),
    C("stone",2,None),
    C("tin",4,"Tools"),
    C("zinc",4,"Chemistry"),
    C("zinc",3,"Electricity"),
    C("iron",3,"Iron Tools"),
    C("aluminium",5,"Aluminium"),
    C("sulphur",5,None),
    C("meteor",200,"Nemesis"),
    C("balrog",100,"Nemesis"),
    C("fuelcrisis",100,"Fire"),
    ]

STOCK = {"animals":ANIMALS,
         "vegetables":VEGETABLES,
         "minerals":MINERALS}

class Recipe():
    __slots__ = ('result','need','gain','keep','points','show')
    def __init__(self,result, gain=None, points=0, need=None, keep=None, show=None):
        self.result = result
        self.need = need
        self.gain = gain
        self.points = points
        self.keep = keep
        self.show = show if show else result

R = Recipe

RECIPES = {
    # ingedients : (get card, need achievement, get achievement, score)
    ("log","stick"):R("wheel","Wheel",10),
    ("flint","stick"):R("spear","Hunting",5),
    ("flint","twigs"):R("ash","Fire",10),
    ("flint","grass"):R("ash","Fire",10),
    ("grass","grass"):R("string"),
    ("salt","skin"):R("leather","Leathercraft",5),
    ("copper","string"):R("copperwire","Wire",30, need="Bronze"),
    ("copperwire","iron"):R("dynamo","Electricity",50),
    ("sand","stone"):R("concrete","Concrete",30, need="Fire"),
    ("concrete","iron"):R("rconcrete","Reinforced Concrete",30),
    ("dynamo","rconcrete"):R("hydroelectric","Renewable Energy",100),
    ("copper","zinc"):R("brass","Alloys",30),
    ("copper","tin"):R("bronze","Bronze",20,need="Fire"),
    ("brass","wheel"):R("gear","Clockwork",50),
    ("bone","string"):R("needle","Sewing",10),
    ("grass","water"):R("paper","Paper",15),
    ("gear","paper"):R("cardmill","Data",50),
    ("clay","clay"):R("pottery","Containers",10,need="Fire"),
    ("cardmill","steamengine"):R("analyticalengine","Computing",100),
    ("coal","ironore"):R("iron","Iron",20,need="Fire"),
    ("coal","sulphur"):R("gunpowder","Explosives",30,need="Fire"),
    ("gunpowder","iron"):R("cannon","Cannon",50),
    ("coal","water"):R("steamengine","Steam",50,need="Iron Tools"),
    ("analyticalengine","cannon"):R("analyticalcannon","Automated Artillery",200),
    ("leather","string"):R("bag","Containers",10),
    ("salt","sand"):R("glass","Glassware",20,need="Fire"),
    ("dirt","grass"):R("compost"),
    ("dirt","twigs"):R("compost"),
    ("dirt","dirt"):R("ironore",need="Chemistry"),
    ("brass","glass"):R("lens","Optics",20),
    ("brass","lens"):R("microscope","Microbiology",50),
    ("lens","lens"):R("telescope","Astronomy",30),
    ("bread","compost"):R("mould"),
    ("microscope","mould"):R("antibiotics","Antibiotics",200),
    ("stick","stick"):R("woodentools","Tools",5),
    ("bronze","stick"):R("bronzetools","Bronze Tools",20),
    ("bronze","woodentools"):R("bronzetools","Bronze Tools",20),
    ("bronzetools","iron"):R("irontools","Iron Tools",20),
    ("iron","stick"):R("irontools","Iron Tools",20),
    ("bronzetools","dirt"):R("farm","Agriculture",20),
    ("dirt","woodentools"):R("farm","Agriculture",20),
    ("dirt","irontools"):R("farm","Agriculture",20),
    ("bronzetools","compost"):R("farm","Agriculture",20),
    ("compost","irontools"):R("farm","Agriculture",20),
    ("farm","log"):R("treefarm","Land Conservation", 100),
    ("stone","wheat"):R("bread","Baking",20,need="Fire"),
    ("bread","water"):R("beer","Brewing",20,need="Fire"),
    ("leather","needle"):R("lederhosen","Clothing",20),
    ("meat","string"):R("sausage","Sausage",10),
    ("beer","lederhosen"):R("oktoberfest","Oktoberfest",500),
    ("beer","sausage"):R("oktoberfest","Oktoberfest",500),
  #  ("latex","sulphur"):R("rubber","Polymers",50,need="Chemistry"),
    ("ash","clay"):R("aluminium","Aluminium",50,need="Electricity"),
    ("water","water"):R("oxygen","Electrolysis",30,need="Electricity",keep="hydrogen",show="hydrogen+oxygen"),
    ("hydrogen","water"):R("liquidh2","Cryogenics",30,need="Electricity"),
    ("hydrogen","hydrogen"):R("liquidh2","Cryogenics",30,need="Electricity"),
    ("oxygen","water"):R("liquido2","Cryogenics",30,need="Electricity"),
    ("oxygen","oxygen"):R("liquido2","Cryogenics",30,need="Electricity"),
    ("liquidh2","liquido2"):R("rocketfuel","Rocket Fuel",20),
    ("aluminium","rocketfuel"):R("rocketstage","Rocket Engines", 50),
    ("rocketstage","rocketstage"):R("rocket","Spaceships",100),
    ("computer","telescope"):R("meteorwarning","Meteor Warning System",100),
    ("meteorwarning","rocket"):R("meteordefence","Meteor Defence System",200),
    ("glass","sand"):R("silicon","Electronics",100,need="Electricity"),
    ("analyticalengine","silicon"):R("computer","Electronic Computer",100),
    ("sulphur","water"):R("sulphuricacid","Chemistry",20,need="Glassware"),
    ("sulphuricacid","zinc"):R("hydrogen"),
    ("coal","hydrogen"):R("chemicals","Organic Chemistry",30,need="Chemistry"),
    ("coal","sulphuricacid"):R("chemicals","Organic Chemistry",30,need="Chemistry"),
    ("blood","chemicals"):R("DNA","Biotechnology",50,need="Microbiology"),
    ("chemicals","meat"):R("DNA","Biotechnology",50,need="Microbiology"),
    ("DNA","chemicals"):R("monstroserum","Mad Science",100,need="Brewing"),
    ("chicken","monstroserum"):R("hugecock","Monster Creation",100),
    ("chemicals","sulphuricacid"):R("explosives","High Explosives",100),
    ("explosives","hugecock"):R("brex","Blastosaurus Rex",500),
    ("clay","stick"):R("tablet","Writing",20),
    ("paper","stick"):R("scroll","Writing",20),
    ("blood","tablet"):R("sigil","Demonology",50,need="Fire"),
    ("blood","scroll"):R("sigil","Demonology",50,need="Fire"),
    ("monstroserum","sigil"):R("abomination",show="awesome"),
    ("coal","oil"):R("paintk","Paint",5),
    ("ironore","oil"):R("paintr","Paint",5),
    ("bone","oil"):R("paintw","Paint",5),
    ("oil","sulphur"):R("painty","Paint",5),
    ("dirt","oil"):R("paintbr","Paint",5),
    ("copper","oil"):R("paintg","Paint",5),
    ("paintr","painty"):R("painto","Paint",5),
}

NEMESES = {
    # nemesis card : (defence, description)
    "winter":("Agriculture","a series of harsh winters. Hunters and gatherers find no food."),
    "meteor":("Meteor Defence System", "a huge meteor."),
    "balrog":("Automated Artillery", "a terrible Balrog. You dug too deep and awoke shadow and flame."),
    "plague":("Antibiotics", "a horrific plague."),
    "deforestation":("Land Conservation", "reckless deforestation."),
    "abomination":("Blastosaurus Rex","an unthinkable abomination."),
    "fuelcrisis":("Renewable Energy","a serious fuel crisis. No energy means no agriculture, no transport: no food."),
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
    useful_cards = set()

    # nemesis cards and ordinary resources are definitely available
    for c in resource_cards:
        if c.need in (None, "Nemesis"):
            reachable_cards.add(c.name)
    # mutually-recursive card and tech searching functions, memoed in reachable_cards and possible_tech
    def can_gain_tech(aname, visited):
        """ can gain tech if it's in a recipe and cards are available """
        if aname in possible_tech:
            if aname:
                logging.debug("I can get {0}".format(aname))
            return True
        if aname in visited:
            logging.warning("loop at {0}".format(aname))
            return False
        visited.add(aname)
        for (c1, c2), recipe in RECIPES.items():
            if recipe.gain != aname:
                continue
            if c1 > c2:
                continue
            logging.debug("I can get {0} if I can craft {1}+{2}".format(aname,c1,c2))
            if can_gain_card(c1,visited) and (c1==c2 or can_gain_card(c2,visited)) and can_gain_tech(recipe.need,visited):
                possible_tech.add(aname)
                reachable_cards.add(recipe.result)
                known_cards.update([c1, c2, recipe.result])
                if recipe.keep:
                    reachable_cards.add(recipe.keep)
                    known_cards.add(recipe.keep)
                return True
        logging.warning("cannot gain {0}".format(aname))
        return False
    
    def can_gain_card(cname,visited=set()):
        """ can gain card if craftable or obtainable in card decks """
        if cname in reachable_cards:
            logging.debug("I can get {0}".format(cname))
            return True
        if cname in visited:
            logging.warning("loop at {0}".format(cname))
            return False
        visited.add(cname)
        for (c1, c2), recipe in RECIPES.items():
            if cname not in (recipe.result, recipe.keep):
                continue
            if c1 > c2:
                continue
            logging.debug("I can get {0} if I can craft {1}+{2}".format(cname,c1,c2))
            if can_gain_card(c1, visited) and (c1==c2 or can_gain_card(c2, visited)) and can_gain_tech(recipe.need,visited):
                possible_tech.add(recipe.gain)
                reachable_cards.add(recipe.result)
                known_cards.update([c1,c2])
                if recipe.keep:
                    reachable_cards.add(recipe.keep)
                    known_cards.add(recipe.keep)
                return True
        for c in resource_cards:
            if cname != c.name:
                continue
            logging.debug("I can get {0} if I can get {1}".format(cname,c.need))
            if can_gain_tech(c.need, visited):
                reachable_cards.add(cname)
                return True
        return False
        logging.warning("cannot gain {0}".format(cname))

    for r in RECIPES.values():
        known_cards.add(r.result)
        if r.keep:
            known_cards.add(r.keep)
    for ingredients in RECIPES:
        known_cards |= set(ingredients)

    for cname, (need, desc) in NEMESES.items():
        if can_gain_tech(need,set()):
            try:
                nemeses.remove(cname)
            except KeyError:
                known_cards.add(cname)
    # examine cards known but obviously not needed for countering nemeses
    for c in known_cards - reachable_cards:
        can_gain_card(c)

    for (c1, c2) in RECIPES:
        if c1 > c2:
            logging.warning("malformed recipe {0} > {1}".format(c1, c2))
        else:
            useful_cards.update([c1,c2])

    cardlist = []
    for c in sorted(known_cards):
        problems = set()
        if c not in reachable_cards:
            problems.add("unavailable")
        if c in nemeses:
            problems.add("nocounter")
        elif c in NEMESES:
            problems.add("nemesis")
        if c not in useful_cards and c not in NEMESES:
            problems.add("useless")
        cardlist.append((c, " ".join(problems)))
    return cardlist

