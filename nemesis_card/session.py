"""
 Player sessions for Nemesis Card game
"""

import random
import copy
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
        try:
            defence, description = recipes.NEMESES[card.name]
            self.message_card = card.name
            if defence not in self.achieved:
                self.lost = True
                self.message = "Your civilization was destroyed by {0}".format(description)
            else:
                self.message = "Your civilization was threatened by {0} Fortunately you were saved by {1}".format(description, defence)
                self.score += card.rarity
        except KeyError:
            # Not a Nemesis card, just add it to the hand
            self.hand.append(card.name)
            self.message = ""
            self.message_card = None

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
        
    def check_recipe(self):
        """ check if a recipe is possible """
        key = tuple(sorted([self.craft1, self.craft2]))
        result = None
        recipe = recipes.RECIPES.get(key)
        if recipe:
            cardname, need_tech, get_tech, points = recipe
            if need_tech is None or need_tech in self.achieved:
                result = recipe
        return result

    def craft_recipe(self):
        """ craft a recipe if possible """
        recipe = self.check_recipe()
        if recipe:
            cardname, need_tech, get_tech, points = recipe
            self.craft1 = None
            self.craft2 = None
            self.hand.append(cardname)
            if get_tech not in self.achieved:
                self.score += points
                self.achieved.append(get_tech)
                self.message = "You have discovered {0}! (+{1} points)".format(get_tech, points)
                self.message_card = ""

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
