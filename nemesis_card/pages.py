from __future__ import print_function

import os
from nemesis_card import bottle
from nemesis_card.bottle import get, post, template

@get("/")
def home_page():
    return template("home_page")


def setup():
    """ set up template and static file directories """
    data = os.path.abspath(os.path.split(__file__)[0] + "/../data")
    print(data)
    @bottle.route("/static/<filepath:path>")
    def static(filepath):
        return bottle.static_file(filepath, data + "/static")
    bottle.TEMPLATE_PATH = [data + "/views"]
    print(bottle.TEMPLATE_PATH)
