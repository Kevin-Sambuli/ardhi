// map options
const lat =  -1.22488;
const lng =  36.827164;

// const lat =  position.coords.latitude;
// const lng =  position.coords.longitude;

let mapOptions = {
    center: [lat, lng],
    zoom: 13 ,
    measureControl: true};

//create the map object
let map = L.map('map' , mapOptions);
map.zoomControl.setPosition('topright');

//addding map tile layers
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {});

var Osm_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,});

var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,});

var Dark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,});

var SmoothDark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,});

var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,}).addTo(map);

// streets
var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']});

//hybrid
var Hybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    maxZoom: 20, subdomains: ['mt0', 'mt1', 'mt2', 'mt3']});

//satellite
var Satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 20, subdomains: ['mt0', 'mt1', 'mt2', 'mt3']});

//terrain
var Terrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
    maxZoom: 20, subdomains: ['mt0', 'mt1', 'mt2', 'mt3'] });

// Raster WMS layers
var wms = L.tileLayer.wms("http://localhost:8080/geoserver/wms", {
    layers: 'counties',
    format: 'image/png',
    transparent: true,
    attribution: "Map by Kevin Sambuli Amuhaya"
}).addTo(map);

// var legend = L.control({position: 'bottomright'}).addTo(map);


//minimap
var osm2 = new L.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    {minZoom: 0, maxZoom: 13, attribution: 'Map By Sambuli Kevin Amuhaya'});
var miniMap = new L.Control.MiniMap(osm2, { toggleDisplay: true }).addTo(map);

// var miniMap = new L.Control.GlobeMiniMap(
//     {
//         land:'#4cae4c',
//         water:'#3333FF',
//         marker:'#000000',
//         topojsonSrc: './world.json'
//     }).addTo(map);


// var magnifyingGlass = L.magnifyingGlass({
//     layers: [osm2]
// });

// map.addLayer(magnifyingGlass);

//adding the tiles to the map
var baseMaps = {
    "Topo": OpenTopoMap,
    "osm": osm,
    "Satellite": Satellite,
    "Terrain": Terrain,
    "Hybrid": Hybrid,
    "osm Mapnik": Osm_Mapnik,
    "Smooth": Stadia_AlidadeSmooth,
    "smooth Dark": SmoothDark,
    "Dark": Dark,
};

// scale control layer
L.control.scale().addTo(map);

// adding a marker
let marker1 = L.marker([lat, lng ],{
    draggable: true,
    title: "marker1",
    opacity: 0.8,
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
    "Marker": marker1,
    // " geojson": geojson
    "Kenya": wms
};

L.control.layers(baseMaps, overLays, {collapsed: false, position: 'topleft' }).addTo(map)


// coordinate display function Map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html(`Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`)
})

// Map Print
$('.print-map').click(function () {
    window.print()
});


//Full screen map view
var mapId = document.getElementById('map');
function fullScreenView() {
    if (document.fullscreenElement) {
        document.exitFullscreen()
    } else {
        mapId.requestFullscreen();
    }
}

//Leaflet browser print function
L.control.browserPrint({ position: 'topright' }).addTo(map);

//Leaflet search
L.Control.geocoder().addTo(map);


//Leaflet measure
L.control.measure({
    position: 'topleft',
    primaryLengthUnit: 'kilometers',
    secondaryLengthUnit: 'meter',
    primaryAreaUnit: 'sqmeters',
    secondaryAreaUnit: undefined
}).addTo(map);

//zoom to layer
$('.zoom-to-layer').click(function () {
    map.setView([lat, lng],13)
})

//getting geolocation and real time tacker
var marker, circle

if(!navigator.geolocation){
    console.log("is not supported")
    } else {
    // setInterval(() => {
    //     navigator.geolocation.getCurrentPosition(getPosition)
    // },5000)
    navigator.geolocation.getCurrentPosition(getPosition)
}

function getPosition(position){
    console.log(position)
    var lat = position.coords.latitude
    var long = position.coords.longitude
    var accuracy = position.coords.accuracy

    // if(marker){
    //     map.removeLayer(marker)
    // }
    //
    // if(circle){
    //     map.removeLayer(circle)
    // }

    var marker = L.Marker([lat, long])
    var circle = L.circle([lat, long], {radius: accuracy})

    var featureGroup = L.featureGroup([marker, circle]).addTo(map)

    map.fitBounds(featureGroup.getBounds())
}


var dataurl = '{% url "data" %}';
$.getJSON(dataurl, function (data) {
    L.geoJson(data, {
        onEachFeature:function(feature, layer)
            {
                layer.bindPopup('<h3 style="align-content: center">Parcel Details</h3>' +
                    '<p>Owner: ' + feature.properties.owner + '</p> ' +
                    '<p>Parcel ID: ' + feature.properties.id + '</p> ' +
                    '<p>Parcel Number: ' + feature.properties.lr_no + '</p> ' +
                    '<p>Status: ' + feature.properties.status + '</p> ' +
                    '<p>Area: ' + feature.properties.area_ha + ' Ha</p>' +
                    '<p>Perimeter: ' + feature.properties.perimeter + ' M</p>').openPopup();
            }
    }).addTo(map);
});