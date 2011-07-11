// An array of texts 
var texts = [];

// The dimensions of the browser.
var dim = { width: $(window).width(), height: $(window).height() };

// Current user position in the universe
// as well as the last position where the texts where updated.
// For the start position, the origin is moved into the middle of the window
var userPos = {x: -Math.round(dim.width/2), y: -Math.round(dim.height/2), lastUpdateX: -Math.round(dim.width/2), lastUpdateY: -Math.round(dim.height/2)};

// The last position and status of the mouse cursor.
var mouse = {x: 0, y: 0, pressed: false};

// The distance that is travelled (in pixels) before updating the view.
var updatePixels = 200;

var universe = '';

function set_universe(uni) {
	universe = uni;
}


/**
 * Retrieves texts from the database as a JSON object.
 * Parses the JSON object to show the texts on screen.
 */
function get_texts() {
	$.post(
		'text/all',
		{ x: userPos.x, y: userPos.y, w: dim.width, h: dim.height, universe: universe },
		function(data) {
			texts = jQuery.parseJSON(data);
			show_texts();
		},
        'json'
	);
}

/**
 * Retrieves user texts from the database as html.
 */
function get_user_texts() {
	$.post(
		'text/mine',
		{ universe: universe },
		function(data) {
			if ($("#user_texts").is(":visible")) {
				$("#user_texts").hide();
				$("#user_texts").html(data);
				$("#user_texts").fadeIn();
			}
			else {
				$("#user_texts").html(data);
			}
		},
        'html'
	);
}

/**
 * Adds some text to the universe
 */
function share_text() {
	var thetext = $("#sharetext").val();
	var theanswer = $("#shareanswer").val();
	$.post(
		'text/share',
		{ text: thetext, answer: theanswer, universe: universe },
		function(data) {
			if (data.length > 0) {
				$("#text_submit").hide();
				$("#text_submit").html(data);
				$("#text_submit").fadeIn();
			}
			//get_user_texts();
			get_texts();
		},
        'html'
	);
    _gaq.push(['_trackEvent', 'Text', 'Share', '', thetext.length]);
}

function fetch_twitter() {
	var thetext = $("#sharetext").val();
	var theanswer = $("#shareanswer").val();
	$.post(
		'text/twitter',
		{ text: thetext, answer: theanswer, universe: universe },
		function(data) {
			if (data.length > 0) {
				$("#text_submit").hide();
				$("#text_submit").html(data);
				$("#text_submit").fadeIn();
			}
			//get_user_texts();
			get_texts();
		},
        'html'
	);
    _gaq.push(['_trackEvent', 'Text', 'TwitterSearch', '', thetext.length]);
}

/**
 * Constructs the html for showing texts.
 */
function show_texts() {
	var res = [];

	// Fetch texts div and clear its contents.
	var textsobj = $('#texts');
	textsobj.html('');

	// Construct a div for each text
	for (i in texts) {
		res.push(
			'<div id="text' + i + '" class="atext"',
			' style="top:' + calc_top_style(texts[i].y) + 'px;',
			'left:' + calc_left_style(texts[i].x) + 'px">',
			texts[i].txt,
			'</div>'
		);
		textsobj.append(res.join(''));
		res = [];
		/*
		if ($('#text' + i).height() >= 50) {
			res.push(
				'<span class="more">',
				'+',
				'</span>'
			);
			$('#text' + i).append(res.join(''));
			res = [];
		}
		*/
	}
}

function calc_top_style(y) {
	return parseInt(y)-userPos.y;
}

function calc_left_style(x) {
	return parseInt(x)-userPos.x;
}


function update_positions(e) {
	if (mouse.pressed) {
		difX = e.clientX-mouse.x
		difY = e.clientY-mouse.y
		userPos.x -= difX;
		userPos.y -= difY;
		for (i in texts) {
			var dd = $('#text'+i);
			var absDivOffset = $(dd).offset();
			$(dd).css('top', absDivOffset.top + difY);
			$(dd).css('left', absDivOffset.left + difX);
		}
		mouse.x = e.clientX;
		mouse.y = e.clientY;
		update_status();
		update_texts();
	}
}

function update_status() {
	$("#status").html('Position of origin: ' + userPos.x + ',' + userPos.y);
}

function update_texts() {
	// Only fetch texts when the screen has been dragged sufficiently.
	update = false;
	if (Math.abs(userPos.x-userPos.lastUpdateX) > updatePixels) {
		update = true;
		userPos.lastUpdateX = userPos.x;
	}

	if (Math.abs(userPos.y-userPos.lastUpdateY) > updatePixels) {
		update = true;
		userPos.lastUpdateY = userPos.y;
	}

	if (update)
		get_texts();
}

function toggle_menu() {
	if ($("#menu").is(":visible")) {
		$("#menu").slideUp();
		$("#menu_toggle").html('show menu');
	}
	else {
		$("#menu").slideDown();
		$("#menu_toggle").html('hide menu');
	}
}

function toggle_about() {
	if ($("#about").is(":visible")) {
		$("#about").fadeOut();
	}
	else {
		$("#user_texts").fadeOut();
		$("#about").fadeIn();
	}
}

function toggle_user_texts() {
	if ($("#user_texts").is(":visible")) {
		$("#user_texts").fadeOut();
	}
	else {
		$("#about").fadeOut();
		get_user_texts();
		$("#user_texts").fadeIn();
	}
}

/**
 * Updates the login html area
 */
function login_html() {
	$.get(
		"login",
		{},
		function(data) {
			if (data.length > 0)
				$("#login").html(data);
		},
        'html'
	);
}

/**
 * Updates the area where text sharing is possible
 */
function share_text_html() {
	$.get(
		'text/share',
		{},
		function(data) {
			if (data.length > 0) {
				$("#text_submit").hide();
				$("#text_submit").html(data);
				$("#text_submit").fadeIn();
			}
		},
        'html'
	);
}

$(document).ready(function() { 
	$("#container").fadeIn();
	login_html();
	share_text_html();
	get_texts();

	$("#texts").mousedown(function(e) {
		$("#overlay").show();
		mouse.x = e.clientX;
		mouse.y = e.clientY;
		mouse.pressed = true;
	});

}); 

$(document).mousemove(function(e) {
	update_positions(e);
});

$(document).mouseup(function(e) {
	mouse.pressed = false;
	$("#overlay").hide();
});
