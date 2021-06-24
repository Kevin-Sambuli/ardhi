// map options
const lat =  -1.22488;
const lng =  36.827164;

// const lat =  position.coords.latitude;
// const lng =  position.coords.longitude;

let mapOptions = {
    center: [lat, lng],
    zoom: 13 };

//create the map object
let map = L.map('map' , mapOptions);


//addding map tile layers
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {});

var Osm_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
});

var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
});

var Dark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
});

var SmoothDark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
});

var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
}).addTo(map);

// streets
var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

//hybrid
var Hybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

//satellite
var Satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

//terrain
var Terrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
});

// Raster WMS layers
// var wms = L.tileLayer.wms("http://localhost:8080/geoserver/wms", {
//     layers: 'counties',
//     format: 'image/png',
//     transparent: true,
//     attribution: "WMS"
// });

var baseMaps = {
    "Topo": OpenTopoMap,
    "osm": osm,
    "Satellite": Satellite,
    "Terrain": Terrain,
    "Hybrid": Hybrid,
    "OSM Mapnik": Osm_Mapnik,
    "Smooth": Stadia_AlidadeSmooth,
    "smooth Dark": SmoothDark,
    "Dark": Dark,
};

// scale control layer
L.control.scale().addTo(map);

// adding a marker
let marker = L.marker([lat, lng ],{
    draggable: true,
    title: "marker",
    // opacity: 0.5
    }).addTo(map).bindPopup('My place');

// GeoJson
// var geojson = L.geoJSON(data, {
//     onEachFeature: function ( feature, layer){
//         layer.bindPopup('<b> Name :</b>' + feature.properties.name)
//     },
//
//     style: {
//         fillColor: 'green',
//         fillOpacity: 0.2,
//         color:'34rrrtc',
//     },
//     }).bindPopup(function (layer) {
//         return layer.feature.properties.description;
//     }).addTo(map);


var overLays = {
    "Marker": marker,
    // " geojson": geojson
    // " wms": wms
};

L.control.layers(baseMaps, overLays, { collapsed: true}).addTo(map)




 // full screen map view
var mapId = document.getElementById('map');
function fullScreenView(){
    mapId.requestFullscreen();
}

// coordinate display function
map.on('mousemove', function (e) {
    $('.coordinate').html('Lat: e.latlng.lat Lng: e.latlng.lng')
});

// Map Print
$('.print-map').click(function () {
    window.print()
});

//browser print
L.control.browserPrint().addTo(map);
L.Control.geocoder().addTo(map);
