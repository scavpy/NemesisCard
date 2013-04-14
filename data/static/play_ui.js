/*
 UI for Nemesis Card game
*/

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

function setup() {
    deal_card("flint");
    deal_card("stick");
    deal_card("flint");
    get_score();
}

$(setup);