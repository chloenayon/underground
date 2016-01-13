var dothing = function(e){
    obj = document.forms['newPlace'];
    obj.elements["location"].value = addThing;
};

function showPosition(pos){
    var a = [pos.coords.latitude, pos.coords.longitude];
    return a;
};

var addThing = function add(e){
    navigator.geolocation.getCurrentPosition(showPosition);
};
