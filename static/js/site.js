$(document).ready(function() {
  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("closed");
  });


  if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(loadMap);
    } else {

      console.log("UGGHH");
    }


});


function loadMap(position) {
  console.log(position)
  L.mapbox.accessToken = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA';
  var map = L.mapbox.map('map', 'mapbox.streets')
  .setView([40.7127, -74.0059], 12);
}
