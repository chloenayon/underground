$(document).ready(function() {
  L.mapbox.accessToken = MAPBOX_TOKEN
  var latitude = $('#mapsm').attr('data-lat');
  var longitude = $('#mapsm').attr('data-lon');
  var category = $('#mapsm').attr('data-cat');

  var map = L.mapbox.map('mapsm', 'mapbox.emerald').setView([latitude, longitude], 12);

  L.marker([latitude, longitude], {
    icon: L.mapbox.marker.icon({
      'marker-symbol': category,
      'marker-size': 'medium',
      'marker-color': '#6d5cae'
    })
  }).addTo(map);


})
