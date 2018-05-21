var geocoder;
var map;
var marker;
var infowindow = new google.maps.InfoWindow({size: new google.maps.Size(150,50)});

function initialize(lat, lon, zoom) {
	geocoder = new google.maps.Geocoder();
	var latlng = new google.maps.LatLng(lat, lon);
	var mapOptions = {
		zoom: zoom,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
	google.maps.event.addListener(map, 'click', function() {
		infowindow.close();
	});
	
	if (infowindow) infowindow.close();
	marker = new google.maps.Marker({
		map: map,
		draggable: true,
		position: latlng,
	});
	google.maps.event.addListener(marker, 'dragend', function() {
		// updateMarkerStatus('Drag ended');
		geocodePosition(marker.getPosition());
	});
	infowindow.setContent("<br>Coordenadas: "+marker.getPosition().toUrlValue(6));
	infowindow.open(map, marker);

	$('#id_geo_location').val(marker.getPosition().toUrlValue(6));
}

function clone(obj){
	if(obj == null || typeof(obj) != 'object') return obj;
	var temp = new obj.constructor(); 
	for(var key in obj) temp[key] = clone(obj[key]);
	return temp;
}


function geocodePosition(pos) {
	geocoder.geocode({
		latLng: pos
	}, function(responses) {
		if (responses && responses.length > 0) {
			marker.formatted_address = responses[0].formatted_address;
		} else {
			marker.formatted_address = 'Esta ubicación no es correcta.';
		}
		infowindow.setContent(marker.formatted_address+"<br>Coordenadas: "+marker.getPosition().toUrlValue(6));
		infowindow.open(map, marker);
	});
	$('#id_geo_location').val(marker.getPosition().toUrlValue(6));
}

function codeAddress() {
	var address = document.getElementById('address').value;
	geocoder.geocode( { 'address': address}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);

			if (marker) {
				marker.setMap(null);
				if (infowindow) infowindow.close();
			}
			marker = new google.maps.Marker({
				map: map,
				draggable: true,
				position: results[0].geometry.location
			});
			google.maps.event.addListener(marker, 'dragend', function() {
				// updateMarkerStatus('Drag ended');
				geocodePosition(marker.getPosition());
			});
			google.maps.event.addListener(marker, 'click', function() {
				if (marker.formatted_address) {
					infowindow.setContent(marker.formatted_address+"<br>coordinates: "+marker.getPosition().toUrlValue(6));
				} else  {
					infowindow.setContent(address+"<br>Coordenadas: "+marker.getPosition().toUrlValue(6));
				}
				infowindow.open(map, marker);
			});
			google.maps.event.trigger(marker, 'click');
			$('#id_geo_location').val(marker.getPosition().toUrlValue(6));
		} else {
			alert('Inserte una dirección no es correcta.');
		}
	});
}