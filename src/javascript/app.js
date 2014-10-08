var $ = require('jquery');
var countdown = require('countdown');
var KeyboardJS = require('keyboardjs');

$(document).ready(function(){
	var latlng = new google.maps.LatLng(-42.886681, 147.336267);

	var markerIcon = {
		path: 'M 0, 0 m -10, 0 a 10,10 0 1,0 20,0 a 10,10 0 1,0 -20,0',
		fillColor: '#5bbb72',
		fillOpacity: 1,
		scale: 1,
		strokeColor: 'transparent'
	  };

	var mapOptions = {
		zoom: 15,
		center: latlng,
		disableDefaultUI: true,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		styles: [{"featureType":"landscape","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","stylers":[{"saturation":-100},{"lightness":51},{"visibility":"simplified"}]},{"featureType":"road.highway","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"road.arterial","stylers":[{"saturation":-100},{"lightness":30},{"visibility":"on"}]},{"featureType":"road.local","stylers":[{"saturation":-100},{"lightness":40},{"visibility":"on"}]},{"featureType":"transit","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"administrative.province","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":-25},{"saturation":-100}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]}]
	};

	var map = new google.maps.Map(document.getElementById('map'), mapOptions);

	var marker = new google.maps.Marker({
		position: latlng,
		map: map,
		title: 'Come say hello!',
		icon: markerIcon
	});

	var $timer = $('.countdown--progress');

	$timer.countdown($timer.data('startdatetime') , function(e) {
		$(this).text( e.strftime('%D Days %H Hours %M Minutes %S Seconds') );
	});

	KeyboardJS.on('ctrl + p', function(){ $('body').toggleClass('is-present-mode'); });
});

