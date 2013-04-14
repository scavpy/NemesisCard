"""
 Player sessions for Nemesis Card game
"""

import random
from collections import defaultdict, deque
from nemesis_card.bottle import request, response

from nemesis_card import recipes

class CardGameSession:
    """ game session, consisting of:
       shuffled decks of resource cards
       player hand
       player achievements
       player score
    """
    MAX_HAND = 13
    def __init__(self):
        self.decks = defaultdict(deque)
        self.hand = []
        self.achieved = []
        self.score = 0
        self.replenish("animals")
        self.replenish("vegetables")
        self.replenish("minerals")

    def nextcard(self, deckname):
        """ get a dictionary of info about next card """
        if len(self.hand) >= self.MAX_HAND:
            return None
        deck = self.decks[deckname]
        if not deck:
            self.replenish(deckname)
        card = deck.popleft()
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

    def replenish(self, deckname):
        stock = recipes.STOCK[deckname]
        #TODO care about rarity
        deck = self.decks[deckname]
        stuff = stock[:]
        random.shuffle(stock)
        for s in stuff:
            deck.append(s)

        
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
