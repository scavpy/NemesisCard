Nemesis Card
===============

Entry in PyWeek #16  <http://www.pyweek.org/16/>
URL: http://pyweek.org/e/nemesis_card
Team: SporkfulofPork
Members: scav
License: LGPL


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py

It will try to open a browser tab on localhost:8123.  If it succeeds and your
default browser is adequate, you can then play the game.


How to Play the Game
--------------------

Can you prepare against pitiless fate?

This is a resource and crafting card game. Each turn you can
draw a resource card (animal, vegetable or mineral) or craft
resources to make tools. Crafting new things gives you civilisation
points, and some things you can craft are important achievements.

Hidden among the resource decks are deadly Nemesis cards. If you draw
one and do not yet have the achievement to counter it, the game is over
and your civilisation is destroyed.

If you attain all the planet-saving achievements before being destroyed,
you win.  This is not guaranteed to be possible every time; life's not
fair.


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

