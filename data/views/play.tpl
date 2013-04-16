<!doctype html>
<head>
 <title>Nemesis Card</title>
 <link rel="stylesheet" href="/static/cards.css"/>
 <script src="/static/jquery-1.9.1.min.js"></script>
 <script src="/static/play_ui.js"></script>
</head>
<body>
 <div id="cardtable">
  <div id="achievements">
   <h2>Achieved</h2>
   <ul id="achieved">
   </ul>
  </div>
  <div id="decks">
   <h2>Resources</h2>
   <div id="animals" class="deck animal"></div>
   <div id="vegetables" class="deck vegetable"></div>
   <div id="minerals" class="deck mineral"></div>
  </div>
  <div id="crafting">
   <h2>Crafting</h2>
   <div id="craft1" class="crafting deck"></div>
   <div id="craft2" class="crafting deck"></div>
   <div id="result" class="result deck"></div>
   <div id="discard" class="discard deck"></div>
  </div>
  <h2>Score <span id="score"></span></h2>
  <ul id="hand">
  </ul>
 <div id="message">
   <div class="leftcol">
     <div id="message_text"></div>
     <button class="dismiss" type="button">Ok</button>
   </div>
   <div class="rightcol">
     <div id="message_card" class="deck"></div>
   </div>
 </div>
 <span class="hidden">{{session}}</span>
</body>
