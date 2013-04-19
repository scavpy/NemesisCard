"""
  WEB PAGES
  ==========
  / - home page and tutorial
  /play - start or continue a game
  /check - list all card images and check they are craftable
  /quit - abandon a game
  
  WEB SERVICES
  ============
  All return a JSON representation of the game state unless otherwise specified
  
  GET
    /state      - current game state
    /craft      - if the cards in the crafting slots make a valid recipe, return card name

  POST
    /draw/D     - Draw from deck D (animals|vegetables|minerals)
    /discard/A  - Discard card at A from the hand, A in {"craft1","craft2", 0..12}
    /move/A/B   - Move a card from A to B. B in {"craft1","craft2","hand"}
    /craft      - craft a new card if the crafting slots hold a valid recipe

"""

import os
import json

from nemesis_card import bottle
from nemesis_card.bottle import get, post, template, abort,redirect

from nemesis_card import session, recipes

@get("/")
def home_page():
    return template("home_page")

@get("/play")
def play_game():
    sessionID = session.start()
    return template("play", session=sessionID)

@get("/quit")
def quit_game():
    session.delete()
    redirect("/")

@get("/check")
def check_cards():
    cardlist = recipes.check_cards()
    return template("check", cards=cardlist)

@get("/probs")
def probabilities():
    probs = session.probabilities()
    return template("probs", probs=probs)

@get("/state")
def get_state():
    state = session.get()
    return json.dumps(state.as_dict())

@post("/discard/<cardpos>")
def discard_card(cardpos=None):
    state = session.get()
    state.discard(cardpos)
    return json.dumps(state.as_dict())

@post("/draw/<deckname>")
def draw_card(deckname=None):
    state = session.get()
    state.draw_card(deckname)
    return json.dumps(state.as_dict())

@post("/move/<frompos>/<topos>")
def move_card(frompos=None,topos=None):
    state = session.get()
    state.move_card(frompos, topos)
    return json.dumps(state.as_dict())

@get("/craft")
def check_recipe():
    game = session.get()
    recipe = game.check_recipe()
    result = recipe[0] if recipe else None
    return json.dumps(result)

@post("/craft")
def craft_recipe():
    game = session.get()
    game.craft_recipe()
    return json.dumps(game.as_dict())

def setup():
    """ set up template and static file directories """
    data = os.path.abspath(os.path.split(__file__)[0] + "/../data")
    @bottle.route("/static/<filepath:path>")
    def static(filepath):
        return bottle.static_file(filepath, data + "/static")
    bottle.TEMPLATE_PATH = [data + "/views"]
