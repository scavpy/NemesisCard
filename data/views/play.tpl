<!doctype html>
<head>
 <title>Nemesis Card</title>
 <link rel="stylesheet" href="/static/cards.css"/>
 <script src="/static/jquery-1.9.1.min.js"></script>
 <script src="/static/play_ui.js"></script>
</head>
<body>
 <div id="cardtable">
  <div id="achieved">
   <h2>Achieved</h2>
  </div>
  <div id="decks">
   <h2>Resources</h2>
   <div id="animal_deck" class="deck animal"></div>
   <div id="vegetable_deck" class="deck vegetable"></div>
   <div id="mineral_deck" class="deck mineral"></div>
  </div>
  <div id="crafting">
   <h2>Crafting</h2>
   <div id="craft1" class="crafting deck"></div>
   <div id="craft2" class="crafting deck"></div>
   <div id="result" class="result deck"></div>
  </div>
  <h2>Score <span id="score"></span></h2>
  <ul id="hand">
  </ul>
 </div>
 <span class="hidden">{{session}}</span>
</body>
