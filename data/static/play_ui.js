/*
 UI for Nemesis Card game
*/
var gamestate = {};

function card_img(cardname, dragpos) {
    var attrs = 'src="/static/' + cardname + '.svg"';
    if (dragpos != null) {
	attrs += ' draggable=true data-pos="' + dragpos + '"';
	attrs += ' ondragstart="start_drag(event)"';
    }
    return '<img  ' + attrs + '>';
}

function deal_card(cardname, cardnum) {
    var hand = $('#hand');
    hand.append('<li class="card">' + card_img(cardname, cardnum) + '</li>');
}

function show_card(deckname, cardname, dragpos) {
    clear_deck(deckname).append(card_img(cardname, dragpos));
}

function start_drag(e) {
    var dt = e.dataTransfer;
    dt.effectAllowed="move";
    dt.setData("text/plain", e.target.getAttribute("data-pos"));
    dt.setDragImage(e.target,60,90);
    return true;
}

function allow_drag(e) {
    e.preventDefault();
}

function discard_drop(e) {
    var dt = e.originalEvent.dataTransfer;
    var frompos = dt.getData("text/plain");
    $.post("/discard/" + frompos, null, got_state, "json");
}

function move_drop(e) {
    var topos = e.target.id;
    var dt = e.originalEvent.dataTransfer;
    var frompos = dt.getData("text/plain");
    $.post("/move/" + frompos + "/" + topos, null, got_state, "json");
}

function accept_recipe(e) {
    $.post("/craft", null, got_state, "json");
}

function clear_deck(deckname) {
    var deck = $('#' + deckname);
    deck.empty();
    return deck;
}

function got_state(state) {
    gamestate = state;
    show_all();
}

function refresh_state() {
    $.get("/state", null, got_state, "json");
}

function draw_card_from_deck(evt) {
    if (gamestate.lost) return;
    $.post("/draw/" + evt.target.id, null, got_state, "json");
}

function show_all() {
    show_achieved()
    show_crafting()
    show_score()
    show_hand()
    show_message()
}

function show_achieved() {
    var achieved = $('#achieved');
    achieved.empty();
    var names = gamestate.achieved;
    for (var i = 0; i < names.length; ++i) {
	achieved.append('<li>' + names[i] + '</li>');
    }
}

function show_crafting() {
    var check = true;
    if (gamestate.craft1) {
	show_card("craft1", gamestate.craft1, "craft1");
    } else {
	clear_deck("craft1");
	check = false;
    }
    if (gamestate.craft2) {
	show_card("craft2", gamestate.craft2, "craft2");
    } else {
	clear_deck("craft2");
	check = false;
    }
    clear_deck("result");
    if (check) {
	$.get("/craft", null, function(cardname) { if (cardname) show_card("result", cardname); }, "json");
    }
}

function show_score() {
    var score = $('#score');
    score.empty();
    score.append(gamestate.score);
}

function show_hand() {
    var hand = $('#hand');
    var cardnames = gamestate.hand;
    hand.empty()
    for (var i = 0; i < cardnames.length; ++i) {
	deal_card(cardnames[i], i);
    }
}

function show_message() {
    var message_para = $('#message_text');
    var vis = gamestate.message ? 'visible' : 'hidden';
    message_para.empty();
    message_para.html(gamestate.message);
    if (gamestate.message_card) {
	show_card('message_card', gamestate.message_card);
    } else {
	clear_deck('message_card');
    }
    $('#message').css('visibility',vis);
}

function dismiss_message() {
    $('#message').css('visibility','hidden');
    if (gamestate.lost) location.href = "/quit";
}

function setup() {
    refresh_state();
    $('#animals').click(draw_card_from_deck);
    $('#vegetables').click(draw_card_from_deck);
    $('#minerals').click(draw_card_from_deck);
    $('#message .dismiss').click(dismiss_message);
    $('.crafting').bind("dragover", allow_drag);
    $('#discard').bind("dragover", allow_drag);
    $('#hand').bind("dragover", allow_drag);
    $('.crafting').bind("drop", move_drop);
    $('#discard').bind("drop", discard_drop);
    $('#hand').bind("drop", move_drop);
    $('#result').mousedown(accept_recipe);
    $('#help_btn').click(function() {$('#howtoplay').toggle("invisible");});
}

$(setup);