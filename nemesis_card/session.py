"""
 Player sessions for Nemesis Card game
"""

import random
from nemesis_card.bottle import request, response

class CardGameSession:
    """ game session, consisting of:
       shuffled decks of resource cards
       player hand
       player achievements
       player score
    """
    def __init__(self):
        self.decks = {
            "animal":["plague"],
            "vegetable":["stick","stick","famine"],
            "mineral":["flint","flint","meteor"]
        }
        self.hand = []
        self.achieved = []
        self.score = 0

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
