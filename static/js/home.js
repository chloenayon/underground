$(document).ready(function() {
  $.get("http://ipinfo.io", function(response) {
    var coords = response.loc.split(',');
    var latitude = parseFloat(coords[0])
    var longitude = parseFloat(coords[1])
    var width = $('section.jumbotron').width()
    var height = $('section.jumbotron').height()
    $('section.jumbotron').css('background-image', 'url(https://api.mapbox.com/v4/mapbox.emerald/'+longitude+','+latitude+',12/'+'1280x1280.jpg?access_token='+MAPBOX_TOKEN+')')
  }, 'jsonp');
});
