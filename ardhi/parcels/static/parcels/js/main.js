var lat = -1.22488;
var lng = 36.827164;

var wfsLayer = new L.featureGroup();
var drawgeojson = new L.featureGroup();
var wfsLayerSearch = new L.featureGroup();
var editableLayers = new L.FeatureGroup();
var layerEditable = new L.FeatureGroup();


// Geoserver settings
var wms_Layer_url = "http://localhost:8080/geoserver/kenya/wms?";
var wfs_layer_url = "http://localhost:8080/geoserver/kenya/ows?"; //add  trailing question when using ajax
var getcaps = "http://localhost:8080/geoserver/kenya/wms?service=wms&version=1.3.0&request=GetCapabilities";
var attribution = "Map by Kevin Sambuli Amuhaya";

// initializing system variables
var queryValue = null;
var geoLayer = null;
var cqlFilter = null;
var selectedArea = null;
var area = null;

// map.addLayer(editableLayers);


var MyCustomMarker = L.Icon.extend({
    options: {
        shadowUrl: null,
        iconAnchor: new L.Point(12, 12),
        iconSize: new L.Point(24, 24),
        iconUrl: 'image/logo.png'
    }
});


var basemaps = {
    "OpenStreetMaps": L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            minZoom: 2,
            maxZoom: 19,
            id: "osm.streets"
        }
    ),
    "Google-Map": L.tileLayer(
        "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}",
        {
            minZoom: 2,
            maxZoom: 19,
            id: "google.street"
        }
    ),
    "Google-Satellite": L.tileLayer(
        "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        {
            minZoom: 2,
            maxZoom: 19,
            id: "google.satellite",
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }
    ),

    "Satellite": L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }
    ),

    "OpenTopoMap": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        {maxZoom: 17}
    ),

    "Terrain": L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }),

    "Google-Hybrid": L.tileLayer(
        "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}",
        {
            minZoom: 2,
            maxZoom: 20,
            id: "google.hybrid",
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }
    ),

    "Terrain": L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        }
    ),

    "Dark": L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        {maxZoom: 20}
    ),
    "OpenTopoMap": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        {maxZoom: 17}
    ),
    "Osm_Mapnik": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {maxZoom: 19,}),

};


// Geojson style file
var myStyle = {
    stroke: true,
    fillColor: '#B04173',
    fillOpacity: 0.5,
    color: 'yellow ',
    weight: 1,
    Opacity: 1.0,
};


//Map Options
var mapOptions = {
    zoomControl: false,
    attributionControl: false,
    center: [lat, lng],
    minZoom: 6.2,
    zoom: 6.2,
    layers: [basemaps.Dark],
};


//create the map object
let map = L.map('map', mapOptions);

// editableLayers.addTo(map);
// layerEditable.addTo(map);


// Get Map's Center
var centerBounds = map.getBounds().getCenter();


// scale control layer
L.control.scale({
    metric: true,
    imperial: false,
    updateWhenIdle: true,
    maxWidth: 200
}).addTo(map);


L.control.zoom({position: "topleft"}).addTo(map);

// Creating an attribution with an Attribution options
var attrOptions = {
    prefix: 'Made by Kevin Sambuli'
};


var attr = L.control.attribution(attrOptions).addTo(map);


//  initializing the side bar
var sidebar = L.control
    .sidebar({
        autopan: true,
        container: "sidebar",
        position: "right"
    })
  // .addTo(map);

// // adding the Lr Number to the Map
// imageBounds = [[-1.22155, 36.8222], [-1.2293, 36.8277]];
// var imageUrl = "{% static 'parcels/image/map.jpg'%}";
// var imgoverlay = L.imageOverlay(imageUrl, imageBounds, {opacity: 1, zIndex: 1});


// function to open up the pop up on draw end
var popup = L.popup({
    closeButton: true,
    autoClose: true,
    className: "custom-popup"
});


var drawOptions = {
    position: "bottomleft",
    draw: {
        polyline: {
            shapeOptions: {
                color: '#f357a1',
                weight: 10,
            },
            metric: true
        },
        // circle: true, // Turns off this drawing tool
        // rectangle: false,
        rectangle: {
            shapeOptions: {
                clickable: false
            }
        },
        marker: true,
        // marker: {icon: new MyCustomMarker()}

        polygon: {
            shapeOptions: {
                stroke: true,
                color: '#f357a1',
                weight: 10,
                lineCap: 'round',
                lineJoin: 'round',
                opacity: 0.5,
                fill: true,
                fillColor: null,
                fillOpacity: 0.2,
                clickable: true
            },
            allowIntersection: false, // Restricts shapes to simple polygons
            drawError: {
                color: "#e1e100", // Color the shape will turn when intersects
                message: "<strong>Oh snap!<strong> you can't draw that!" // Message that will show when intersect
            },
            showArea: true,
            showLength: true,
            strings: `['ha', 'm']`,
            metric: true,
            feet: false,
            nautic: false,
            // repeatMode: true,
            precision: {km: 2, ft: 0}

        }
    },

    // edit:false
    edit: {
        featureGroup: editableLayers, //REQUIRED!!
        remove: true,
        poly: {
            allowIntersection: false
        }
    }
};

var drawControl = new L.Control.Draw(drawOptions);