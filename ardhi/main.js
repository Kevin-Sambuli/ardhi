// map options
const lat = -1.22488;
const lng = 36.827164;

// const lat =  position.coords.latitude;
// const lng =  position.coords.longitude;

let mapOptions =
    {
        center: [lat, lng],
        zoom: 13,
        // measureControl: true,
        // zoomsliderControl: true,
    };

//create the map object
let map = L.map('map', mapOptions);

map.zoomControl.setPosition('topleft');


var sidebar = L.control.sidebar('sidebar', {
            closeButton: true,
            position: 'left'
        });
        map.addControl(sidebar);

        setTimeout(function () {
            sidebar.show();
        }, 500);

        var marker2 = L.marker([lat, lng]).addTo(map).on('click', function () {
            sidebar.toggle();
        });

        map.on('click', function () {
            sidebar.hide();
        })

        sidebar.on('show', function () {
            console.log('Sidebar will be visible.');
        });

        sidebar.on('shown', function () {
            console.log('Sidebar is visible.');
        });

        sidebar.on('hide', function () {
            console.log('Sidebar will be hidden.');
        });

        sidebar.on('hidden', function () {
            console.log('Sidebar is hidden.');
        });

        L.DomEvent.on(sidebar.getCloseButton(), 'click', function () {
            console.log('Close button clicked.');
        });

//addding map tile layers
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {});

var Osm_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19,});

var Stadia_AlidadeSmooth = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {
    maxZoom: 20});

var Dark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {maxZoom: 20});

var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {maxZoom: 17})

// // streets
var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20, subdomains: ['mt0', 'mt1', 'mt2', 'mt3']});

// //hybrid
var Hybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']});

//satellite
var Satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']}).addTo(map);

//terrain
var Terrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']});

//minimap
var miniMap = new L.Control.MiniMap(osm, {toggleDisplay: true}).addTo(map);





// creating the style layer to the counties shapefile
var county_style = `<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" version="1.1.0" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>counties</se:Name>
    <UserStyle>
      <se:Name>counties</se:Name>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>Single symbol</se:Name>
          <se:LineSymbolizer>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000000</se:SvgParameter>
              <se:SvgParameter name="stroke-width">3</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
              <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
            </se:Stroke>
          </se:LineSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:TextSymbolizer>
            <se:Label>
              <ogc:PropertyName>countyname</ogc:PropertyName>
            </se:Label>
            <se:Font>
              <se:SvgParameter name="font-family">Mongolian Baiti</se:SvgParameter>
              <se:SvgParameter name="font-size">15</se:SvgParameter>
            </se:Font>
            <se:LabelPlacement>
              <se:PointPlacement>
                <se:AnchorPoint>
                  <se:AnchorPointX>0</se:AnchorPointX>
                  <se:AnchorPointY>0.5</se:AnchorPointY>
                </se:AnchorPoint>
              </se:PointPlacement>
            </se:LabelPlacement>
            <se:Halo>
              <se:Radius>2</se:Radius>
              <se:Fill>
                <se:SvgParameter name="fill">#666666</se:SvgParameter>
              </se:Fill>
            </se:Halo>
            <se:Fill>
              <se:SvgParameter name="fill">#19f1c6</se:SvgParameter>
            </se:Fill>
            <se:VendorOption name="maxDisplacement">1</se:VendorOption>
          </se:TextSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
`

// var wfsLayer = L.tileLayer.wfs("http://localhost:8080/geoserver/wfs",{
var wfsLayer = L.Geoserver.wfs("http://localhost:8080/geoserver/wfs", {
    layers: "kenya:parks",
    style:
        {
            color: "green",
            fillColor: "green",
            fillOpacity: "0.5",
            opacity: "0.5",
        },
    onEachFeature: function (feature, layer) {
        area = (turf.area(feature)/1000000).toFixed(2);
        // cent= turf.center(feature),
        // bbox= turf.BBOX(feature),

        // lat = turf.center(feature).geometry.coordinates[1]
        // long = turf.center(feature).geometry.coordinates[0]
        layer.bindPopup('<h3 style="align-content: center">Parcel Details</h3>' +
                                    '<p>Fid: ' + feature.properties.fid + '</p> ' +
                                    '<p>Area: ' + area + ' ' + 'sqkm' + '</p>' +
                                    // '<p>Lat: ' + lat +'</p>' +
                                    // '<p>Long: ' + long + '</p>' +
                                    '<p>Park: ' + feature.properties.parkname + '</p> ');
    },

    });
// wfsLayer.addTo(map);

// Raster WMS layers
var forests = L.Geoserver.wms("http://localhost:8080/geoserver/wms",
// var wms = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'forests',
        format: 'image/png',
        transparent: true,
        attribution: "Map by Kevin Sambuli Amuhaya"
    }).addTo(map);


var airports = L.Geoserver.wms("http://localhost:8080/geoserver/wms",
// var airports = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'airports',
        format: 'image/png',
        // transparent: true,
        // attribution: "Map by Kevin Sambuli Amuhaya"
    }).addTo(map);

// var wms = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
var counties = L.Geoserver.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'counties',
        format: 'image/png',
        // style : county_style,
        // CQL_FILTER: "countycode=='47'",
        transparent: true,
        attribution: "Map by Kevin Sambuli Amuhaya"
    }).addTo(map);

var soils = L.Geoserver.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'soils',
        format: 'image/png',
        transparent: true,
        attribution: "Map by Kevin Sambuli Amuhaya"
    }).addTo(map);

var population = L.Geoserver.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'population',
        format: 'image/png',
        transparent: true,
        attribution: "Map by Kevin Sambuli Amuhaya"
    }).addTo(map);



//legend request
var legend = L.Geoserver.legend("http://localhost:8080/geoserver/wfs",
    {
        layers: 'population',
        // style: stylefile,
    })
// legend.addTo(map);


//adding the tiles to the map
var baseMaps = {
    "OSM": osm,
    "Topo": OpenTopoMap,
    "Satellite": Satellite,
    "Terrain": Terrain,
    "Hybrid": Hybrid,
    "osm Mapnik": Osm_Mapnik,
    "Smooth": Stadia_AlidadeSmooth,
    "Dark": Dark,
};

// // adding a markers to the map
// let marker = L.marker([lat, lng], {
//     draggable: true,
//     title: "marker",
//     opacity: 0.8,
// })
// marker.addTo(map).bindPopup('My place');



var overLays = {
    "County": counties,
    "Population": population,
    "Forests": forests,
    "Parks": wfsLayer,
    "Soils": soils,
    "Airports": airports,
};

L.control.layers(baseMaps, overLays, {collapsed: true, position: 'topright'}).addTo(map);

//Leaflet browser print function
L.control.browserPrint({position: 'topright'}).addTo(map);

//Leaflet search
L.Control.geocoder().addTo(map);

// leaflet locate user location
L.control.locate().addTo(map);

// scale control layer
L.control.scale().addTo(map);




// //Leaflet measure
L.control.measure({
        // position: 'topleft',
        primaryLengthUnit: 'kilometers',
        secondaryLengthUnit: 'meter',
        primaryAreaUnit: 'sqmeters',
        secondaryAreaUnit: undefined
    }).addTo(map);




// coordinate display function Map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html(`Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`)
});

//zoom to layer
$('.zoom-to-layer').click(function () {
    map.setView([lat, lng], 13)
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

// add Leaflet-Geoman controls with some options to the map

map.pm.addControls({
  position: 'topleft',
  drawCircle: false,
    snappingOption: true,
});


// getting geolocation and real time tacker
var marker2, circle

if (!navigator.geolocation) {
    console.log("is not supported")
} else {

    // setInterval(() => {
    //     navigator.geolocation.getCurrentPosition(getPosition)
    // },5000)

    navigator.geolocation.getCurrentPosition(getPosition)
};

function getPosition(position) {
    // console.log(position)
    var lat = position.coords.latitude;
    var long = position.coords.longitude;
    var accuracy = position.coords.accuracy;

    // if(marker){
    //     map.removeLayer(marker)
    // }
    //
    // if(circle){
    //     map.removeLayer(circle)
    // }

    var marker2 = L.marker([lat, long],
        {
            draggable: false,
            title:"marker",
            opacity:0.8,
        }).bindPopup('My place');

    var circle = L.circle([lat, long], {radius: accuracy});
    var featureGroup = L.featureGroup([marker2, circle])
    // featureGroup.addTo(map);

    map.fitBounds(featureGroup.getBounds());
}

// getfeatureinfo event
var ms_url = "http://localhost/geoserver/kenya/ows?"
map.addEventListener('click', Identify);

//getting wmf features from geoserver using ajax
function Identify(e) {
    // set parameters needed for GetFeatureInfo WMS request
    var BBOX = map.getBounds().toBBoxString();
    var WIDTH = map.getSize().x;
    var HEIGHT = map.getSize().y;
    var X = map.layerPointToContainerPoint(e.layerPoint).x;
    var Y = map.layerPointToContainerPoint(e.layerPoint).y;
    // compose the URL for the request
    var URL = ms_url + 'SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&LAYERS=countries&QUERY_LAYERS=counties&BBOX='
        + BBOX + '&FEATURE_COUNT=1&HEIGHT=' + HEIGHT + '&WIDTH='
        + WIDTH + '&INFO_FORMAT=text%2Fhtml&SRS=EPSG%3A4326&X=' + X + '&Y=' + Y;

    //send the asynchronous HTTP request using jQuery $.ajax
    $.ajax({
        url: URL,
        dataType: "html",
        type: "GET",
        success: function (data) {
            var popup = new L.Popup({
                maxWidth: 300
            });
            popup.setContent(data);
            popup.setLatLng(e.latlng);
            map.openPopup(popup);
        },
    })
};

var geojsonStyle =
    {
        fillColor:"ff7800",
        color:"#000",
        weight:1,
        opacity: 1,
        fillOpacity:0.8
    };

// var data = "http://localhost:8080/geoserver/kenya/ows?service=wfs&version=2.0.0&request=GetFeature&typeNames=kenya:counties&outputFormat=application/json"

var url = "http://localhost:8080/geoserver/kenya/ows?";
var service = "wfs&";
var version = "2.0.0&";
var request = "GetFeature&";
var typeNames = "kenya:counties&";
var outputFormat = "application/json";
var count = 50;
// var sortBy = countyname;
var srsName= "epsg:4326";
// var dataUrl = url + service + version + request + request + outputFormat



// $.getJSON(dataUrl).then(res)=> {
//     var layer = L.geoJson(res,{
//         onEachFeature:function (feature, layer) {
//             layer.bindPopup(feature.properties.countyname),
//         },
//         style: geojsonStyle
//     }).addTo(map);
//     map.fitBounds(layer.getBounds());
// }




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


//            function map_init_basic(map, options) {
//              var geojsonPointLayer = new L.GeoJSON.AJAX("{% url 'data' %}", {
//                 onEachFeature: function (feature, layer) {-->
//                  layer.bindPopup(feature.properties.name.toString());
//               },
//             });
//              geojsonPointLayer.addTo(map);
//           }



// var wms = 'http://localhost:8080/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
// var wfs = 'http://localhost:8080/geoserver/wfs?service=wfs&version=1.1.0&request=GetCapabilities'

// vector WFS layers

// var wfs = L.Geoserver.wfs("http://localhost:8080/geoserver/wfs",
//     {
//         layers: 'counties',
//         style :
//             {
//                 // color:"black",
//                 fillOPacity:"0.3",
//                 fillColor:"green"
//                 opacity:"o.5"
//             },
        // onEachfeature: function (feature, layer)
        //                     {
        //                         layer.bindPopup('<h3 style="align-content: center">Counties</h3>' +
        //                                 '<p>Owner: ' + feature.properties.countyname + '</p> ' +
        //                                 '<p>Parcel ID: ' + feature.properties.id + '</p> ' +
        //                                 '<p>Parcel Number: ' + feature.properties.lr_no + '</p> ' +
        //                                 '<p>Status: ' + feature.properties.status + '</p> ' +
        //                                 '<p>Area: ' + feature.properties.area_ha + ' Ha</p>' +
        //                                 '<p>Perimeter: ' + feature.properties.perimeter + ' M</p>').openPopup();
        //                     },
        // CQL_FILTER: "countycode=='47'",
    // }).addTo(map);



// global minimap
// var miniMap = new L.Control.GlobeMiniMap(
//     {
//         land:'#4cae4c',
//         water:'#3333FF',
//         marker:'#000000',
//         topojsonSrc: './world.json'
//     });
