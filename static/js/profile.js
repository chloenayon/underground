$(document).ready(function() {
  L.mapbox.accessToken = MAPBOX_TOKEN;

  $.get("http://ipinfo.io", function(response) {
    var coords = response.loc.split(',');
    var latitude = parseFloat(coords[0])
    var longitude = parseFloat(coords[1])

    map = L.mapbox.map('map', 'mapbox.emerald').setView([latitude, longitude], 12);
    myLayer = L.mapbox.featureLayer().addTo(map);

    myLayer.on('layeradd', function(e) {
      var marker = e.layer,
        properties = marker.feature.properties;

        console.log(marker)

      // Create custom popup content
      var popupContent = '<a href="/places/' + properties.id + '">' + properties.name + '</a><br><p>' + properties.description + '</p>' + '<br><p>' + marker.feature.geometry.coordinates[0] + ',' + marker.feature.geometry.coordinates[1] + '</p><br><p>'+properties.address+'</p>';

      // http://leafletjs.com/reference.html#popup
      marker.bindPopup(popupContent, {
        closeButton: true,
        minWidth: 320
      });
    });

    // Add features to the map
    myLayer.setGeoJSON(geoJson);
  }, 'jsonp');

});
