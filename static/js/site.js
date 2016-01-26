MAPBOX_TOKEN = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA';

$(document).ready(function() {
  $('select').select2();
  $("a[data-target=\"#searchModal\"]").click(function(){
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(fillAddPlace);
    }
  })

});

function fillAddPlace(position) {
  // $('#addPlaceForm input[name="latitude"]').val(position.coords.latitude)
  // $('#addPlaceForm input[name="longitude"]').val(position.coords.longitude)

  $.getJSON('https://api.mapbox.com/geocoding/v5/mapbox.places/'+longitude+','+latitude+'.json?access_token='+MAPBOX_TOKEN, function(data) {
    var place = data.features[0];

    if (place) {
      $('#addPlaceForm input[name="name"]').val(place.text)
      $('#addPlaceForm input[name="latitude"]').val(place.center[0])
      $('#addPlaceForm input[name="longitude"]').val(place.center[1])
      $('#addPlaceForm input[name="address"]').val(place.place_name)
    } else {

    }

  })
}

function loadMap(position) {
  console.log(position)
  L.mapbox.accessToken = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA';
  var map = L.mapbox.map('map', 'mapbox.streets')
  .setView([40.7127, -74.0059], 12);
}
