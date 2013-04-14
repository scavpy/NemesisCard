<!doctype html>
<head>
 <title>Nemesis Card</title>
 <link rel="stylesheet" href="/static/cards.css"/>
</head>
<body>
 <h1><b>Nemesis Card</b></h1>
 <div id="cardtable">
  <button id="play_btn" class="play" onClick="location.href='/play'">
   Play
  </button>
  <h2>How To Play</h2>
  <p>Play consists of drawing resource cards and crafting them into
  new cards, which may be used for further crafting or as tools with
  special uses.</p>
  <p>There are three decks of resource cards:
   Animal, Vegetable and Mineral.</p>
  <div class="deck animal"></div> 
  <div class="deck vegetable"></div> 
  <div class="deck mineral"></div> 
  <p>You will need a good mix of all three
   kinds, but you can only hold 13 cards at a time, so if you have a full
   hand you must discard one before drawing another. Crafting sometimes
   uses up a card, so that is another option if your hand is full.</p>
  <p>You craft new cards by placing two of the cards in your hand into the
   crafting area and if that combination of cards is a valid crafting
   recipe, then a third card will appear.
  <div class="deck crafting">
   <img src="/static/stick.svg">
  </div>
  <div class="deck crafting">
   <img src="/static/flint.svg">
  </div>
  <div class="deck result ok">
   <img src="/static/spear.svg">
  </div>
  <p>If you accept that card then one or both of the cards you placed
   in the crafting area will disappear and the newly crafted card will
   go into your hand.</p>
  <p>Discovering new crafting recipes adds to your score and your list
  of achievements, and makes more advanced recipes possible. Just because
  you can't combine two cards now doesn't mean you will never be able to.
  For example, the range of recipes available to you increases quite a bit
  after you discover fire :)</p>
  <p>But beware.  Lurking in the resource decks are the deadly
  <em>Nemesis</em> cards.</p>
  <div class="deck"><img src="/static/nemesis.svg"></div>
  <p>If you draw one of these and have not attained
  the technological achievement necessary to avert the catastrophe
  represented by that card, your civilisation is destroyed and your game
  is over.</p>
  <button id="play_btn" class="play" onClick="location.href='/play'">
   Play
  </button>
 </div>
</body>
