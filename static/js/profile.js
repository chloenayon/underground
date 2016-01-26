$(document).ready(function() {
  L.mapbox.accessToken = MAPBOX_TOKEN

  $.get("http://ipinfo.io", function(response) {
    var coords = response.loc.split(',');
    var latitude = parseFloat(coords[0])
    var longitude = parseFloat(coords[1])

    var map = L.mapbox.map('map', 'mapbox.emerald').setView([latitude, longitude], 12);
  })
});
