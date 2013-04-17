<!doctype html>
<head>
 <title>Nemesis Card</title>
 <link rel="stylesheet" href="/static/cards.css"/>
 <script src="/static/jquery-1.9.1.min.js"></script>
</head>
<body>
 <div id="cardtable">
  %for cardname, classes in cards:
     <img src="/static/{{cardname}}.svg" class="check {{classes}}" title="{{cardname}} {{classes}}">
  %end
 </div>
</body>
