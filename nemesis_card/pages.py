from __future__ import print_function

import os
import json

from nemesis_card import bottle
from nemesis_card.bottle import get, post, template, request, response
import nemesis_card.session

@get("/")
def home_page():
    return template("home_page")

@get("/play")
def play_game():
    sessionID = nemesis_card.session.start()
    return template("play", session=sessionID)

@get("/achieved")
def get_achieved():
    achieved = nemesis_card.session.get().achieved
    return json.dumps(achieved)

@get("/score")
def get_score():
    score = nemesis_card.session.get().score
    return json.dumps(score)

def setup():
    """ set up template and static file directories """
    data = os.path.abspath(os.path.split(__file__)[0] + "/../data")
    @bottle.route("/static/<filepath:path>")
    def static(filepath):
        return bottle.static_file(filepath, data + "/static")
    bottle.TEMPLATE_PATH = [data + "/views"]
