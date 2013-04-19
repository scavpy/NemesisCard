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
    C("log",2,None),
    C("wheat",5,None),
#    C("latex",2,None),
    C("deforestation",500,"Nemesis"),
    ]

ANIMALS = [
    C("skin",1,"Hunting"),
#    C("ivory",1,"Hunting"),
    C("bone",3,None),
    C("chicken",10,None),
    C("plague",500,"Nemesis"),
 #   C("snake",1,None),
    C("meat",10,"Hunting"),
    C("blood",20,"Containers"),
    C("DNA",10,"Microbiology"),
    ]

MINERALS = [
    C("dirt",1,None),
    C("water",1,"Containers"),
    C("clay",5,None),
    C("flint",2,None),
    C("sand",3,None),
    C("salt",5,None),
    C("copper",10,None),
    C("ironore",10,None),
    C("coal",5,"Bronze Tools"),
    C("stone",1,None),
    C("tin",5,None),
    C("zinc",5,"Electricity"),
    C("iron",3,"Iron Tools"),
    C("aluminium",5,"Aluminium"),
    C("sulphur",10,None),
    C("meteor",1000,"Nemesis"),
    C("balrog",500,"Nemesis"),
    ]

STOCK = {"animals":ANIMALS,
         "vegetables":VEGETABLES,
         "minerals":MINERALS}

RECIPES = {
    # ingedients : (get card, need achievement, get achievement, score)
    ("log","stick"):("wheel",None,"Wheel",10),
    ("flint","stick"):("spear",None,"Hunting",5),
    ("flint","twigs"):("ash",None,"Fire",10),
    ("flint","grass"):("ash",None,"Fire",10),
    ("grass","grass"):("string",None,None,0),
    ("salt","skin"):("leather",None,"Leathercraft",0),
    ("copper","string"):("copperwire","Bronze","Wire",30),
    ("copperwire","iron"):("dynamo",None,"Electricity",50),
    ("copper","zinc"):("brass",None,"Alloys",30),
    ("copper","tin"):("bronze","Fire","Bronze",20),
    ("brass","wheel"):("gear",None,"Clockwork",50),
    ("bone","string"):("needle",None,"Sewing",10),
    ("grass","water"):("paper",None,"Paper",15),
    ("gear","paper"):("cardmill",None,"Data",50),
    ("cardmill","steamengine"):("analyticalengine",None,"Computing",100),
    ("coal","ironore"):("iron","Fire","Iron",20),
    ("coal","sulphur"):("gunpowder","Fire","Explosives I",30),
    ("gunpowder","iron"):("cannon",None,"Cannon",50),
    ("coal","water"):("steamengine","Iron","Steam",50),
    ("analyticalengine","cannon"):("analyticalcannon",None,"Automated Artillery",200),
    ("leather","string"):("bag",None,"Containers",10),
    ("salt","sand"):("glass","Fire","Glassware",20),
    ("dirt","grass"):("compost",None,None,0),
    ("dirt","twigs"):("compost",None,None,0),
    ("brass","glass"):("lens",None,"Optics",20),
    ("brass","lens"):("microscope",None,"Microbiology",50),
    ("lens","lens"):("telescope",None,"Astronomy",30),
    ("bread","compost"):("mould",None,None,0),
    ("microscope","mould"):("antibiotics",None,"Antibiotics",200),
    ("bronze","stick"):("bronzetools",None,"Bronze Tools",20),
    ("bronzetools","iron"):("irontools",None,"Iron Tools",20),
    ("iron","stick"):("irontools",None,"Iron Tools",20),
    ("bronzetools","dirt"):("farm",None,"Agriculture",20),
    ("dirt","irontools"):("farm",None,"Agriculture",20),
    ("farm","log"):("treefarm",None,"Land Conservation", 100),
    ("stone","wheat"):("bread","Fire","Baking",20),
    ("bread","water"):("beer","Glassware","Brewing",20),
    ("leather","needle"):("lederhosen",None,"Clothing",20),
    ("beer","lederhosen"):("oktoberfest",None,"Oktoberfest",500),
  #  ("latex","sulphur"):("rubber","Chemistry","Polymers",50),
    ("ash","clay"):("aluminium","Electricity","Aluminium",50),
  #  ("aluminium","rubber"):("airtightsuit","Clothing",None,0),
  #  ("airtightsuit","glass"):("spacesuit",None,"Spacesuit",100),
    ("water","water"):("hydrogen+oxygen","Electricity","Electrolysis",30),
    ("hydrogen","water"):("liquidh2","Electricity","Cryogenics",30),
    ("oxygen","water"):("liquido2","Electricity","Cryogenics",30),
    ("liquidh2","liquido2"):("rocketfuel",None,"Rocket Fuel",20),
    ("aluminium","rocketfuel"):("rocketstage",None,"Rocket Engines", 50),
    ("rocketstage","rocketstage"):("rocket",None,"Spaceships",50),
    ("computer","telescope"):("meteorwarning",None,"Meteor Warning System",100),
    ("meteorwarning","rocket"):("meteordefence",None,"Meteor Defence System",200),
    ("glass","sand"):("silicon","Electricity","Electronics",100),
    ("analyticalengine","silicon"):("computer",None,"Electronic Computer",100),
    ("sulphur","water"):("sulphuricacid","Glassware","Chemistry",20),
    ("coal","hydrogen"):("chemicals","Chemistry","Advanced Chemistry",30),
    ("blood","chemicals"):("DNA","Microbiology","Biotechnology",50),
    ("chemicals","meat"):("DNA","Microbiology","Biotechnology",50),
    ("DNA","chemicals"):("monstroserum","Brewing","Mad Science",100),
    ("chicken","monstroserum"):("hugecock",None,"Monster Creation",100),
    ("chemicals","sulphuricacid"):("explosives",None,"Explosives II",100),
    ("explosives","hugecock"):("brex",None,"Blastosaurus Rex",500),
    ("clay","stick"):("tablet",None,"Writing",20),
    ("paper","stick"):("scroll",None,"Writing",20),
    ("blood","tablet"):("sigil","Fire","Demonology",50),
    ("blood","scroll"):("sigil","Fire","Demonology",50),
    ("monstroserum","sigil"):("abomination",None,None,0),
}

NEMESES = {
    # nemesis card : (defence, description)
    "meteor":("Meteor Defence System", "a huge meteor."),
    "balrog":("Automated Artillery", "a terrible Balrog. You dug too deep and awoke shadow and flame."),
    "plague":("Antibiotics", "a horrific plague."),
    "deforestation":("Land Conservation", "reckless deforestation."),
    "abomination":("Blastosaurus Rex","an unthinkable abomination."),
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
        logging.debug("can I get {0}?".format(aname))
        if aname in possible_tech:
            logging.debug("yes")
            return True
        if aname in visited:
            logging.warning("loop at {0}".format(aname))
            return False
        visited.add(aname)
        for (c1, c2), (c3, need, gain, pts) in RECIPES.items():
            if gain != aname:
                continue
            logging.debug("I can get {0} if I can craft {1}+{2} into {3}".format(aname,c1,c2,c3))
            results = c3.split("+")
            if c1 <= c2 and can_gain_card(c1,visited) and can_gain_card(c2,visited) and can_gain_tech(need,visited):
                possible_tech.add(aname)
                reachable_cards.update(results)
                known_cards.update(results + [c1, c2])
                return True
        logging.warning("cannot gain {0}".format(aname))
        return False
    
    def can_gain_card(cname,visited=set()):
        """ can gain card if craftable or obtainable in card decks """
        if cname in reachable_cards:
            return True
        logging.debug("can I get {0}?".format(cname))
        if cname in visited:
            logging.warning("loop at {0}".format(cname))
            return False
        visited.add(cname)
        for (c1, c2), (c3, need, gain, pts) in RECIPES.items():
            results = c3.split("+")
            if not cname in results:
                continue
            logging.debug("I can get {0} if I can craft {1}+{2} into {3}".format(cname,c1,c2,c3))
            if c1 <= c2 and can_gain_card(c1) and can_gain_card(c2) and can_gain_tech(need,visited):
                possible_tech.add(gain)
                reachable_cards.update(results)
                known_cards.update([c1,c2])
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
        known_cards |= set(r[0].split("+"))
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
        if c not in useful_cards and c not in NEMESES:
            problems.add("useless")
        cardlist.append((c, " ".join(problems)))
    return cardlist

