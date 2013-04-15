/*
 UI for Nemesis Card game
*/
var gamestate = {"lost":false, "craft1":null, "craft2":null};
var cardnumber = 0;

function card_img(cardname, draggable) {
    var id = "card" + (++cardnumber);
    return '<img src="/static/' + cardname + '.svg" ' +
	(draggable ? 'draggable=true ' : '') + 
	'data-card="' + cardname + '" ' +
	'id="' + id + '">' ;
}

function deal_card(cardname) {
    var hand = $('#hand');
    hand.append('<li class="card">' + card_img(cardname, true) + '</li>');
    $('#hand img').bind('dragstart', start_drag);
}

function show_card(deckname, cardname) {
    clear_deck(deckname).append(card_img(cardname));
}

function start_drag(e) {
    var dt = e.originalEvent.dataTransfer;
    dt.effectAllowed="move";
    dt.setData("Text", e.target.id);
    dt.setDragImage(e.target,0,0);
    return true;
}

function allow_drag(e) {
    e.preventDefault();
}

function name_of_card(cardid) {
    return $('#' + cardid).attr("data-card");
}

function check_drop(e) {
    var id = e.target.id;
    var dt = e.originalEvent.dataTransfer;
    var cardid = dt.getData("Text");
    var cardname = name_of_card(cardid);
    if (id == "discard") {
	discard(cardid);
    } else if (gamestate[id] == null) {
	gamestate[id] = cardname;
	show_card(id, cardname);
	if (gamestate["craft1"] && gamestate["craft2"]) {
	    check_recipe();
	}
    }
}

function check_recipe() {
    function got_recipe(obj) {
	if (obj) {
	    show_card("result", obj);
	} else {
	    clear_deck("result");
	}
    }
    $.get("/craft/" + gamestate["craft1"] + "+" + gamestate["craft2"],
	  null, got_recipe, "json");
}

function discard(cardid) {
    var cardname = name_of_card(cardid);
    $.post("/discard/" + cardname, null, get_hand);
    clear_crafting();
}

function clear_deck(deckname) {
    var deck = $('#' + deckname);
    deck.empty();
    return deck;
}

function clear_crafting() {
    clear_deck("craft1");
    clear_deck("craft2");
    clear_deck("result");
    gamestate["craft1"] = null;
    gamestate["craft2"] = null;
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
    $('.crafting').bind("dragover", allow_drag);
    $('#discard').bind("dragover", allow_drag);
    $('.crafting').bind("drop", check_drop);
    $('#discard').bind("drop", check_drop);
}

$(setup);