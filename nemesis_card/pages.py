import os
import json

from nemesis_card import bottle
from nemesis_card.bottle import get, post, template, abort

from nemesis_card import session

@get("/")
def home_page():
    return template("home_page")

@get("/play")
def play_game():
    sessionID = session.start()
    return template("play", session=sessionID)

@get("/achieved")
def get_achieved():
    achieved = session.get().achieved
    return json.dumps(achieved)

@get("/score")
def get_score():
    score = session.get().score
    return json.dumps(score)

@post("/draw/<deckname>")
def draw_card(deckname=None):
    game = session.get()
    try:
        deck = game.decks[deckname]
    except KeyError:
        abort(404, "no such deck")
    nextcard = game.nextcard(deckname)
    return json.dumps(nextcard)

def setup():
    """ set up template and static file directories """
    data = os.path.abspath(os.path.split(__file__)[0] + "/../data")
    @bottle.route("/static/<filepath:path>")
    def static(filepath):
        return bottle.static_file(filepath, data + "/static")
    bottle.TEMPLATE_PATH = [data + "/views"]
