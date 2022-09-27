var map;

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


// Map Options
var mapOptions = {
    zoomControl: false,
    attributionControl: false,
    center: [-1.22488, 36.827164],
    minZoom: 6.2,
    zoom: 6.2,
    layers: [basemaps.Dark],
};



//create the map object
map = L.map('map', mapOptions);


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





// Geojson style file
var myStyle = {
    stroke: true,
    fillColor: '#B04173',
    fillOpacity: 0.5,
    color: 'yellow ',
    weight: 1,
    Opacity: 1.0,
};


// Get Map's Center
var centerBounds = map.getBounds().getCenter();



// var counties = L.tileLayer.wms("http://localhost:8080/geoserver/kenya/wms",
//     {
//         layers: 'kenya:counties',
//         format: 'image/png',
//         tiled: true,
//         transparent: true,
//         attribution: attribution
//     }).addTo(map);
//
// var population = L.tileLayer.wms("http://localhost:8080/geoserver/kenya/wms",
//     {
//         layer: 'kenya:population',
//         format: 'image/png',
//         transparent: true,
//         tiled: true,
//         opacity: 0.6,
//         zIndex: 100,
//         attribution: attribution
//     }).addTo(map);
//
// var nairobiPlots = L.tileLayer.wms("http://localhost:8080/geoserver/kenya/wms",
//     {
//         layer: 'kenya:nairobi',
//         format: 'image/png',
//         transparent: true,
//         tiled: true,
//         opacity: 0.6,
//         zIndex: 100,
//         attribution: attribution
//     }).addTo(map);




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


// function to open up the pop up on draw end
var popup = L.popup({
    closeButton: true,
    autoClose: true,
    className: "custom-popup"
});

// define custom marker
var MyCustomMarker = L.Icon.extend({
    options: {
        shadowUrl: null,
        iconAnchor: new L.Point(12, 12),
        iconSize: new L.Point(24, 24),
        iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Information_icon4_orange.svg'
    }
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
        // marker: true,
        marker: {icon: new MyCustomMarker()},

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
                timeout: 3000,
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

// adding the draw custom controls to the map
var drawControl = new L.Control.Draw(drawOptions);


// adding the FR  to the Map
// imageBounds = [[-1.22155, 36.8222], [-1.2293, 36.8277]];
// var imageUrl = "{% static 'parcels/image/map.jpg'%}";
// var imgoverlay = L.imageOverlay(imageUrl, imageBounds, {opacity: 1, zIndex: 1});

// toggle between full screen and normal screen
var mapId = document.getElementById('map');

function fullScreenView() {
    if (document.fullscreenElement) {
        document.exitFullscreen()
    } else {
        mapId.requestFullscreen();
    }
}


var options = {
    position: 'bottomleft',
    drawMarker: true,
    drawPolygon: true,
    drawPolyline: true,
    drawCircle: true,
    editPolygon: true,
    deleteLayer: true
};

// L.control.layers(basemaps, overLays, {collapsed: true, position: 'topright'}).addTo(map);

// map.pm.addControls(options);

// map.on('pm:create', function(e) {
//   // var marker = e.polygon;
//   console.log(e)
//   console.log(e.layer.getLatLngs()[0])
//   editableLayers.addLayer(e.layer);
//   console.log(JSON.stringify(e.layer.toGeoJSON().geometry));
//
//   var type = e.shape
//       console.log(type)
//
// });


//     var container = L.DomUtil.create('input');
//     container.type="button";
//
//     container.title="No cat";
//     container.value = "42";
//
//     container.onmouseover = function(){
//       container.style.backgroundColor = 'pink';
//     }
//     container.onmouseout = function(){
//       container.style.backgroundColor = 'white';
//     }


// <!DOCTYPE html>
// <html>
// <head>
// 	<title>Fit Bounds to Selected Feature</title>
// 	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
// 	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css">
//     <script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js"></script>
//     <style>
//         body {
//             padding: 0;
//             margin: 0;
//         }
//         html, body, #map {
//             height: 100%;
//             width: 100%;
//         }
//         .sel {
// 			padding: 6px 8px;
// 			font: 14px/16px Arial, Helvetica, sans-serif;
// 			background-color: rgba(255,255,255,0.8);
// 			box-shadow: 0 0 15px rgba(0,0,0,0.2);
// 			border-radius: 5px;
// 		}
//     </style>
// </head>
// <body>
// 	<div id="map"></div>
// 	<script>
//
// // Map
// var map = L.map("map").setView([0, 0], 1);
//
// // Tile layer
// L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
// 	maxZoom: 19,
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// }).addTo(map);
//
// // Lines GeoJSON
// var lines = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":1},"geometry":{"type":"LineString","coordinates":[[-113.90625,34.30714385628804],[-106.5234375,47.754097979680026],[-84.375,39.36827914916014]]}},{"type":"Feature","properties":{"id":2},"geometry":{"type":"LineString","coordinates":[[90.3515625,66.23145747862573],[121.28906250000001,61.77312286453146]]}},{"type":"Feature","properties":{"id":3},"geometry":{"type":"LineString","coordinates":[[8.0859375,15.284185114076433],[23.203125,28.613459424004414],[3.1640625,30.14512718337613],[27.7734375,21.289374355860424]]}}]};
//
// // Lines layer
// var line_layer = L.geoJSON(
//     lines, {
//         onEachFeature: function(feature, layer) {
//             layer._leaflet_id = feature.properties.id;
//             layer.bindPopup("<b>ID:</b> " + feature.properties.id, {closeOnClick: false, autoClose: false});
//         },
//         style: {
//             weight: 10
//         }
//     }
// ).addTo(map);
//
// // Open popups
// line_layer.eachLayer(function(layer) {layer.openPopup()});
//
// // Selection menu
// var dropdown = L.control({position: "topright"});
// dropdown.onAdd = function(map) {
//     var div = L.DomUtil.create("div", "sel");
//     div.innerHTML =
//         '<input type="radio" name="id" value="1"> 1<br>' +
//         '<input type="radio" name="id" value="2"> 2<br>' +
//         '<input type="radio" name="id" value="3"> 3';
//     return div;
// };
// dropdown.addTo(map);
//
// // Fit bounds on selection change
// document
//     .querySelector(".sel")
//     .addEventListener(
//         "change",
//         function(e) {
//             var bounds = line_layer.getLayer(e.target.value).getBounds();
//             map.flyToBounds(bounds);
//         }
//     );
//
// 	</script>
// </body>
// </html>


