/*
 UI for Nemesis Card game
*/
var gamestate = {"lost":false};

function card_img(cardname) {
    return '<img src="/static/' + cardname + 
	'.svg" data-card="' + cardname + '">';
}

function deal_card(cardname) {
    var hand = $('#hand');
    hand.append('<li class="card">' + card_img(cardname) + '</li>');
}

function show_card(deckname, cardname) {
    clear_deck(deckname).append(card_img(cardname));
}

function clear_deck(deckname) {
    var deck = $('#' + deckname);
    deck.empty();
    return deck;
}

function get_score() {
    function show_score(rsp) {
	var score = $('#score');
	score.empty();
	score.append(rsp);
    }
    $.get("/score", show_score);
}

function get_achievements() {
    function show_achieved(names) {
	var achieved = $('#achieved');
	achieved.empty();
	for (var i = 0; i < names.length; ++i) {
	    achieved.append('<li>' + names[i] + '</li>');
	}
    }
    $.get("/achieved", null, show_achieved, "json");
}

function draw_card_from_deck(evt) {
    if (gamestate.lost) return;
    var id = evt.target.id;
    function got_card(obj) {
	if (obj.lost) {
	    show_card(id, obj.card);
	    gamestate.lost = true;
	} else {
	    deal_card(obj.card);
	}
    }
    $.post("/draw/" + id, null, got_card, "json");
}

function get_hand() {
    function got_hand(cardnames) {
	var hand = $('#hand');
	hand.empty()
	for (var i = 0; i < cardnames.length; ++i) {
	    deal_card(cardnames[i]);
	}
    }
    $.get("/hand", null, got_hand, "json");
}


function setup() {
    get_score();
    get_achievements();
    get_hand();
    $('#animals').click(draw_card_from_deck);
    $('#vegetables').click(draw_card_from_deck);
    $('#minerals').click(draw_card_from_deck);
}

$(setup);