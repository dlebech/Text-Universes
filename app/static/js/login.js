function start_signup() {
	$.get(
		"./php/login.php",
		{ signup : 'true' },
		function(data) {
			if (data.length > 0)
				$("#login").html(data);
		}
	);
}

function login() {
	username = $("#username").val();
	userpass = $("#userpass").val();
	$.post(
		"/dreams/login",
		{ username : username, password: userpass },
		function(data) {
			if (data.length > 0)
				$("#login").html(data);
		});
}

function signup() {
	username = $("#username").val();
	userpass = $("#userpass").val();
	eml = $("#email").val();
	captcha = $("#captcha_code").val();
	$.post(
		"./php/login.php",
		{ user: username, pass: userpass, email: eml, captcha_code: captcha, signup : 'true' },
		function(data) {
			if (data.length > 0)
				$("#login").html(data);
		}
	);
}

function logout() {
	$.get(
		"dreams/logout",
		{},
		function(data) {
			if (data.length > 0)
				$("#login").html(data);
		}
	);
}
