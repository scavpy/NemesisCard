<!doctype html>
<head>
 <title>Nemesis Card</title>
 <link rel="stylesheet" href="/static/cards.css"/>
 <script src="/static/jquery-1.9.1.min.js"></script>
</head>
<body>
 <div id="cardtable">
   <ul>
     %for deck, psurvive in probs.items():
     <li>{{deck}} - {{psurvive}}</li>
     %end
   </ul>
 </div>
</body>
