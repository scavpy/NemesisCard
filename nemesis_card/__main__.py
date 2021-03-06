from __future__ import print_function

import time
import webbrowser
import argparse
import threading
import logging
from functools import partial

# Using the Bottle framework
from nemesis_card import bottle

# These modules set up the bottle routing
import nemesis_card.pages

def open_browser_later(port, delay=1):
    time.sleep(delay)
    webbrowser.open("http://localhost:{0}".format(port))

def main():
    """ Start the web server and open a browser tab """
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--port", default=8123, type=int, help="Local port number")
    add("--no-open", default=False, action="store_true", help="don't open browser tab")
    add("--debug", default=False, action="store_true", help="show debug log")
    add("--cheat", default=False, action="store_true", help="allow cheats")
    args = ap.parse_args()
    nemesis_card.pages.setup(args.cheat)
    if not args.no_open:
        opener =  threading.Thread(target=partial(open_browser_later, args.port))
        opener.daemon = True
        opener.start()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    bottle.run(host="localhost", port=args.port, debug=True)
