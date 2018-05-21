window.fbAsyncInit = function() {
	FB.init({ appId: '',
		status: true,
		cookie: true,
		xfbml: true,
		user_about_me: true,
		oauth: true
	});

	function updateButton(response) {
		var button = document.getElementById('fb-auth');

		if (response.authResponse) {
			//user is already logged in and connected
			FB.api('/me', function(response) {
				console.log(response)
				$.ajax({
					type:'POST',
					url:'/accounts/user_redsocial/ajax/',
					data:'fbID=' + response.id + '&email=' + response.email + '&fname=' + response.first_name + '&lname=' + response.last_name + '&gender=' + response.gender + '&verified=' + response.verified + '&locale=' + response.locale + '&birthday=' + response.birthday,
					success: function(msg){
						console.log('ok')
					}
				});
				button.innerHTML = 'Logout';
				setTimeout(function(){
					button.innerHTML = 'Logout';
				}, 500);
			});

			$('#logout').click(function(){
				FB.logout(function(response) {
					//var userInfo = document.getElementById('user-info');
					window.location = '/logout/';
				});
			});

			button.onclick = function() {
				FB.logout(function(response) {
					//var userInfo = document.getElementById('user-info');
					window.location = '/logout/';
				});
			};
		} else {
			//user is not connected to your app or logged out
			button.innerHTML = 'Login';
			button.onclick = function() {
				FB.login(function(response) {
					if (response.authResponse) {
						FB.api('/me', function(response) {
							//var userInfo = document.getElementById('user-info');
							//userInfo.innerHTML = '<img src="https://graph.facebook.com/' + response.id + '/picture" style="margin-right:5px"/>' + response.name;
						});
					} else {
						//user cancelled login or did not grant authorization
						alert('Ha cancelado el login.');
					}
				}, {scope:'email,user_birthday,status_update,publish_stream,user_about_me'});
			}
		}
	}
	// run once with current status and whenever the status changes
	FB.getLoginStatus(updateButton);
	FB.Event.subscribe('auth.statusChange', updateButton);
};
/*
(function() {
	var e = document.createElement('script'); e.async = true;
	e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
	document.getElementById('fb-root').appendChild(e);
}());*/
