"""
 Player sessions for Nemesis Card game
"""

import random
import copy
import logging
from nemesis_card.bottle import request, response

from nemesis_card import recipes

class CardStock:
    """ A set of cards that can be selected from randomly """
    def __init__(self, cards):
        self.allcards = cards
        self.picklist = []
        self.allowed = set()
        self.allow(None)

    def allow(self, criterion):
        if criterion in self.allowed:
            return
        newcards = set(c for c in self.allcards if c.need == criterion)
        self.picklist.extend([(1.0/c.rarity, c) for c in newcards])
        self.allowed.add(criterion)

    def pick(self):
        totaldensity = sum(p[0] for p in self.picklist)
        target = random.uniform(0, totaldensity)
        tot = 0.0
        for d, card in self.picklist:
            tot += d
            if tot >= target:
                return card
        return picklist[-1][1]

    def allow_all(self):
        all_criteria = set(c.need for c in self.allcards)
        for a in all_criteria:
            self.allow(a)

    def pnemesis(self):
        allfreq = sum(p[0] for p in self.picklist)
        nemeses = [p for p in self.picklist if p[1].name in recipes.NEMESES]
        logging.debug(nemeses)
        nemesisfreq = sum(n[0] for n in nemeses)
        return nemesisfreq / allfreq


class CardGameSession:
    """ game session, consisting of:
       shuffled decks of resource cards
       player hand
       player achievements
       player score
    """
    MAX_HAND = 13
    SAFE_DRAWS = 40
    def __init__(self):
        self.decks = {
            "animals":CardStock(recipes.ANIMALS),
            "vegetables":CardStock(recipes.VEGETABLES),
            "minerals":CardStock(recipes.MINERALS)
            }
        self.hand = []
        self.achieved = []
        self.score = 0
        self.draws = 0
        self.lost = False
        self.message = ""
        self.message_card = None
        self.craft1 = self.craft2 = None

    def as_dict(self):
        """ Game state as a JSON-ready dictionary """
        d = copy.deepcopy(self.__dict__)
        del d["decks"]
        return d
        
    def draw_card(self, deckname):
        """ Draw a card if possible,
        and if it's a special card, adjust the
        game state accordingly. """
        if deckname not in self.decks:
            return
        ncards = len(self.hand) + (self.craft1 is not None) + (self.craft2 is not None)
        if ncards < self.MAX_HAND:
            deck = self.decks[deckname]
            card = deck.pick()
        else:
            self.message = "Your hand is full"
            self.message_card = None
            return
        self.draws += 1
        if self.draws == self.SAFE_DRAWS:
            for deck in self.decks.values():
                deck.allow("Nemesis")
            self.message = "Your Nemesis approaches. Beware."
            self.message_card = "nemesis"
        else:
            self.message = ""
            self.message_card = None
        self.check_nemesis(card.name, card.rarity)
        
    def check_nemesis(self, cardname, rarity):
        """ see if a newly drawn or crafted card is a nemesis,
        and if so, whether the player has any defence against it. """
        try:
            defence, description = recipes.NEMESES[cardname]
            self.message_card = cardname
            if defence not in self.achieved:
                self.lost = True
                self.message = ("Your civilization was destroyed by {0}.<br>"
                                "If only you had discovered {1}!".format(description, defence))
            else:
                self.message = ("Your civilization was threatened by {0}.<br>"
                                "Fortunately you were saved by {1}".format(description, defence))
                self.score += rarity
        except KeyError:
            # Not a Nemesis card, just add it to the hand
            self.hand.append(cardname)

    def discard(self, cardpos):
        """ discard a card from the hand or crafting slots """
        self.message = ""
        if cardpos == "craft1":
            self.craft1 = None
        elif cardpos == "craft2":
            self.craft2 = None
        else:
            try:
                n = int(cardpos)
                self.hand[n:n+1] = []
            except (ValueError, IndexError):
                pass

    def move_card(self, frompos, topos):
        """
        frompos can be a card position in the hand or a crafting slot
        topos can be a crafting slot or "hand"
        """
        self.message = ""
        # pick up card
        card = None
        if frompos == "craft1" and self.craft1 is not None:
            card = self.craft1
            self.craft1 = None
        elif frompos == "craft2" and self.craft2 is not None:
            card = self.craft2
            self.craft2 = None
        else:
            try:
                n = int(frompos)
                if n >=0 and n < len(self.hand):
                    card = self.hand[n]
                    self.hand[n:n+1] = []
            except (ValueError, IndexError):
                pass
        if card is None:
            return # nothing useful can be done
        # put down card
        if topos == "hand":
            self.hand.append(card)
        elif topos == "craft1":
            if self.craft1 is not None:
                self.hand.append(self.craft1)
            self.craft1 = card
        elif topos == "craft2":
            if self.craft2 is not None:
                self.hand.append(self.craft2)
            self.craft2 = card
        
    def check_recipe(self, fake=False):
        """ check if a recipe is possible """
        key = tuple(sorted([self.craft1, self.craft2]))
        result = None
        recipe = recipes.RECIPES.get(key)
        if recipe:
            cardname, need_tech, get_tech, points = recipe
            if need_tech is None or need_tech in self.achieved:
                result = recipe
            else:
                logging.debug("need {0} to make {1}".format(need_tech, cardname))
                if fake:
                    result = ("q", need_tech, None, 0)
            if fake and cardname == "abomination":
                # you think you are getting something awesome, then...
                result = ("awesome",None,None,0)
        else:
            logging.debug("rejected recipe {0}+{1}".format(key[0],key[1]))
        return result

    def craft_recipe(self):
        """ craft a recipe if possible """
        recipe = self.check_recipe()
        if recipe:
            self.craft1 = None
            self.craft2 = None
            result, need_tech, get_tech, points = recipe
            if get_tech is not None and get_tech not in self.achieved:
                self.score += points
                self.achieved.append(get_tech)
                self.message = "You have discovered {0}! (+{1} points)".format(get_tech, points)
                self.message_card = ""
                for deck in self.decks.values():
                    deck.allow(get_tech)
            for cardname in result.split("+"):
                self.check_nemesis(cardname,1000)

    def cheat(self, cheatcards):
        for cardname in cheatcards:
            self.check_nemesis(cardname,0)

SESSIONS = {}

def start():
    sessionID = request.cookies.get("NemesisCardSession","")
    if not sessionID:
        sessionID = hex(random.getrandbits(64))[2:]
        response.set_cookie("NemesisCardSession", sessionID)
    if sessionID not in SESSIONS:
        SESSIONS[sessionID] = CardGameSession()
    return sessionID

def get():
    sessionID = request.cookies.get("NemesisCardSession","")
    return SESSIONS[sessionID]

def delete():
    sessionID = request.cookies.get("NemesisCardSession","")
    if sessionID:
        try:
            del SESSIONS[sessionID]
        except KeyError:
            pass
        response.set_cookie("NemesisCardSession","")

def probabilities():
    """ probability of surviving 100 draws
    from each deck, assuming you have all the
    tech needed to get any card """
    return {"Animals":psurvive(recipes.ANIMALS, 100),
            "Vegetables":psurvive(recipes.VEGETABLES,100),
            "Minerals":psurvive(recipes.MINERALS,100)}

def psurvive(deck, turns):
    """
    probability of surviving a number of turns from a deck
    """
    stock = CardStock(deck)
    stock.allow_all()
    pnem = stock.pnemesis()
    logging.debug("P(nemesis) = {0}".format(pnem))
    pOK = 1 - pnem
    return pOK ** turns
