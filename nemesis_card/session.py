"""
 Player sessions for Nemesis Card game
"""

import random
from collections import defaultdict
from nemesis_card.bottle import request, response

from nemesis_card import recipes

class CardStock:
    """ A set of cards that can be selected from randomly """
    def __init__(self, cards):
        self.allcards = cards
        self.allowed = set(c for c in cards if c.need is None)

    def allow(self, criterion):
        newcards = set(c for c in self.allcards if c.need == criterion)
        self.allowed |= newcards

    def pick(self):
        totaldensity = sum((1.0 / c.rarity) for c in self.allowed)
        picklist = [(1.0 / c.rarity, c) for c in self.allowed]
        target = random.uniform(0, totaldensity)
        tot = 0.0
        for d, card in picklist:
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
    SAFE_DRAWS = 50
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

    def nextcard(self, deckname):
        """ get a dictionary of info about next card """
        if len(self.hand) >= self.MAX_HAND:
            return None
        deck = self.decks[deckname]
        card = deck.pick()
        self.draws += 1
        if self.draws >= self.SAFE_DRAWS:
            deck.allow("Nemesis")
        response = dict(card=card.name, lost=False)
        try:
            defence = recipes.DEFENCES[card.name]
            if defence not in self.achieved:
                response["lost"] = True
        except KeyError:
            pass
        if not response["lost"]:
            self.hand.append(card)
        return response
        
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
