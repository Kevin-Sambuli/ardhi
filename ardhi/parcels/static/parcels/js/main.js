

var lat = -1.22488;
var lng = 36.827164;

//Map Options
var mapOptions = {
    zoomControl: false,
    attributionControl: false,
    center: [lat, lng],
    minZoom: 6.2,
    zoom: 6.2,
    layers: [basemaps.Dark],
    // maxBounds: [[-4.609278, 34.18650],[4.6311, 42.14463]],
    // maxBoundsViscosity: 1.0, // disabling excess panning out of the max bounds
};

//create the map object
let map = L.map('map', mapOptions);

// disabling double clicking to zoom
// map.doubleClickZoom.disable();

// Get Map's Center
var centerBounds = map.getBounds().getCenter();
// map.setView(centerBounds, 6);

// scale control layer
L.control.scale({
    metric: true,
    imperial: false,
    updateWhenIdle: true,
    maxWidth: 200
}).addTo(map);

//Render Zoom Control zoom control options
L.control.zoom({position: "topleft"}).addTo(map);

//zoom to extent button
// $(".default-view").on("click", function () {
//     map.fitBounds(selectedArea.getBounds());
// });

// allow the map tto perform events on key board events
// $(document).ready(function () {
//     $("input[type=text]").val("");
//     $(".alert").hide();
//     $("#search-value").on("keydown", function (e) {
//         //if user presses Enter Key (keycode 13) on keyboard
//         if( e.keyCode == 13 ) {
//             e.preventDefault();
//             searchWFS();
//         }
//     });
// });

// $('#toolbar .hamburger').on('click', function () {
//     $(this).parent().toggleClass('open');
// });

//mouse hover coordinates
map.on("mousemove", function (e) {
    $(".map-coordinate").html("Lat : " + e.latlng.lat + " Lng : " + e.latlng.lng);
});

// Attribution options
var attrOptions = {
    prefix: 'Made by Kevin Sambuli'
};

// Creating an attribution
var attr = L.control.attribution(attrOptions).addTo(map);
// attr.setPrefix('aasssss').addTo(map);

// var sidebar = L.control
//   .sidebar({
//     autopan: true,
//     container: "sidebar",
//     position: "right"
//   })
//   .addTo(map);


// initializing system variables
var queryValue = null;
var geoLayer = null;
var cqlFilter = null;
var selectedArea = null;
var area = null;


var wfsLayer = new L.featureGroup();
var drawgeojson = new L.featureGroup();
var wfsLayerSearch = new L.featureGroup();
// var editableLayers = new L.FeatureGroup().addTo(map);
var layerEditable = new L.FeatureGroup().addTo(map);
// map.addLayer(editableLayers);

//feature group that contains the editable layer
// editableLayers.addTo(map);
// layerEditable.addTo(map);

// var editableLayers = new L.FeatureGroup();
// var layerEditable = new L.FeatureGroup();

var MyCustomMarker = L.Icon.extend({
    options: {
        shadowUrl: null,
        iconAnchor: new L.Point(12, 12),
        iconSize: new L.Point(24, 24),
        iconUrl: 'image/logo.png'
    }
});

// add Leaflet-Geoman controls with some options to the map
// map.pm.addControls({
//   position: 'topright',
//   drawCircle: false,
//     snappingOption: true,
// });
//
// map.on('pm:create', function(e) {
//     // alert('pm:create event fired. See console for details');
//     console.log('pm',e.layer);
//     console.log('shape',e.layer.getLatLngs()[0]);
// //     layer.on('pm:edit', (e) => {
// //   // if(e.shape === 'Polygon'){
// //   //    (e.layer as Polygon).getLatLngs();
// //   // }
// // });
// });


var editableLayers = new L.FeatureGroup();
// var layerEditable = new L.FeatureGroup();

var drawOptions = {
  position: "bottomleft",
  draw: {
    polyline:  {
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
            stroke:true,
            color: '#f357a1',
            weight: 10,
            lineCap:'round',
            lineJoin:'round',
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
        showArea:true,
        showLength: true,
        strings : `['ha', 'm']`,
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
    poly : {
      allowIntersection : false
    }
  }
};


//adding the draw control with options to the map
var drawControl = new L.Control.Draw(drawOptions);
// map.addControl(drawControl);


// $('.leaflet-prevent').on('click', L.DomEvent.stopPropagation);
// var pinToggler = true;
// $('.pin').on('click', function (e) {
//    if(pinToggler){
//        map.on('click', function(e) {
//            console.log('map clicked')
//            map.addControl(drawControl);
//        }
//        pinToggler = !pinToggler;
//    } else {
//        map.removeControl(drawControl);
//        map.off('click')}
//     }
// });


// coordinate display function Map coordinate display
map.on('click', function (e) {
    $('.mapclicks').html(`Lat: ${e.latlng.lat} <br>Lng: ${e.latlng.lng}`)
    // map.flyTo([e.latlng.lat, e.latlng.lng], 12);
    console.log("map clicked at", `Lat: ${e.latlng.lat}  Lng: ${e.latlng.lng}`)
});


// Edit Button Clicked
var drawToggler = true;
$('#draw').click(function (e) {
    if (drawToggler) {
        //on click we add the draw control layer to the map controls
        map.addControl(drawControl);

        // adding the feature class draw layer
        editableLayers.addTo(map);

        //removing the the geojson layer when drawing the second time
        map.removeLayer(drawgeojson);

        //re assinging the toggle button to make the button to run the else code
        drawToggler = !drawToggler;
        console.log("control added to the map");
    } else {
        // runs when the draw toggle is false
        console.log("control removed  from the map");

        // when the draw toggle is set to false we remove the darw controls
        // from the map and assigning the toggle back to true
        map.removeControl(drawControl);
        map.off('click');
        drawToggler = true;
    }
});

// adding the Lr Number to the Map
imageBounds = [[-1.22155, 36.8222], [-1.2293, 36.8277]];
var imageUrl = 'image/map.jpg';
var imgoverlay = L.imageOverlay(imageUrl, imageBounds, {opacity: 1, zIndex: 1});
// layerControl.addBaseLayer(imgoverlay, 'Georeferenced');
// imgoverlay.addTo(map);
// imgoverlay.bringToBack();
// L.control.layers.addBaseLayer(imgoverlay, 'Georeferenced');

//changing the image opacity using the range input
$('#imgOpacity').on('change', function () {
    $('#image-opacity').html(this.value);
    imgoverlay.setOpacity(this.value);
});

// L.tileLayer('image/png',{
//     attribution: 'Georeferenced Image',
//     // tms:true
//     }).addTo(map);

// //Leaflet measure
// L.control.measure({
//         // position: 'topleft',
//         primaryLengthUnit: 'kilometers',
//         secondaryLengthUnit: 'meter',
//         primaryAreaUnit: 'sqmeters',
//         secondaryAreaUnit: undefined
//     }).addTo(map);


// $('#draw').dblclick(function(e) {
//     map.removeControl(drawControl);
//     //  $(".leaflet-draw").fadeToggle("fast", "linear");
//     //  $(".leaflet-draw-toolbar").fadeToggle("fast", "linear");
//     // this.blur();
//   return true;
// });

// var polygon = turf.polygon([[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]);
// var centroid = turf.centroid('centroid',polygon);


// exportting the layers into the file system
document.getElementById('export').onclick = function (e) {
    // on export you remove the draw feature group
    map.removeLayer(editableLayers);

    //remove the draw controls when exporting the map
    map.removeControl(drawControl);
    var data = editableLayers.toGeoJSON();


    // ploting the drawn shape as a geojson file on the map
    function onEachFeature(feature, layer) {
        // does this feature have a property named popupContent?
        if (feature.properties && feature.properties.lrnumber) {
            // var centroid = turf.centroid(feature.geometry.coordinates);
            // console.log(centroid);
            var popContent =
                "<div" +
                // "<div style='background-image: url(image/gis.jpg);' " +
                "<h3 style='color: aliceblue'><b>Land Parcels</b></h3><hr>" +
                "<b>Number: </b>" + feature.properties.lrnumber + "</br>" +
                "<b>Parcel Id: </b>" + feature.properties.parcelid + "</br>" +
                "<b>Area: </b>" + feature.properties.area + "</br>" +
                "<b>Perimeter: </b>" + feature.properties.parcelid +
                "</div>";
            layer.bindPopup(popContent);
        }
    };

    // Extract GeoJson from featureGroup and display the drawn layers as a geojson
    var DrawGeoJSON = L.geoJson(editableLayers.toGeoJSON(), {
        onEachFeature: onEachFeature,
        style: mySearchStyle,
    }).addTo(drawgeojson);
    drawgeojson.addTo(map); //adding the drawn geojson to the map
    map.fitBounds(drawgeojson.getBounds()); // fitting the map to the bounds of the drawn geojson

    // Stringify the GeoJson
    // var convertedData = 'text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data));

    // Create export
//     document.getElementById('export').setAttribute('href', 'data:' + convertedData);
//     document.getElementById('export').setAttribute('download','data.geojson');

    // make POST ajax call
    //     $.ajax({
    //         type: 'POST',
    //         url: "{% url 'post_parcels' %}",
    //         url: "http://localhost:63342/Ardhi/ardhi/parcels/templates/map.html?_ijt=d9kuvqfrt9iaccuv9t7n4u9vn4",
    //         data: {'data': data}, //data = JSON.stringify(editableLayers.toGeoJSON())
    //         success: function (e) {
    //             console.log('successful logging',JSON.stringify(editableLayers.toGeoJSON(), null, 4) )
    //             alert('success', JSON.stringify(editableLayers.toGeoJSON()))
    //             // editableLayers.bindPopup(layer.feature.properties).openPopup();
    //         },
    //         error : function() {
    //             alert('error', JSON.stringify(editableLayers.toGeoJSON()))
    //         }
    //     });
}


// toggle btwn full screen and normal screen
var mapId = document.getElementById('map');

function fullScreenView() {
    if (document.fullscreenElement) {
        document.exitFullscreen()
    } else {
        mapId.requestFullscreen();
    }
}

// $(".lock-map").click(function () {
//   $(".lock-map").innerHTML('h')
// });


//View map in full browser
function fullScreenToggler() {
    var doc = document,
        elm = document.getElementById("map");

    if (elm.requestFullscreen) {
        !doc.fullscreenElement ? elm.requestFullscreen() : doc.exitFullscreen();
    } else if (elm.mozRequestFullScreen) {
        !doc.mozFullScreen ? elm.mozRequestFullScreen() : doc.mozCancelFullScreen();
    } else if (elm.msRequestFullscreen) {
        !doc.msFullscreenElement
            ? elm.msRequestFullscreen()
            : doc.msExitFullscreen();
    } else if (elm.webkitRequestFullscreen) {
        !doc.webkitIsFullscreen
            ? elm.webkitRequestFullscreen()
            : doc.webkitCancelFullscreen();
    } else {
        console.log("Fullscreen support not detected.");
    }
}

// $(".full-screen").click(fullScreenToggler);


//Browser print
// L.control.browserPrint().addTo(map);
$(".print-map").click(function () {
    var printMode = L.control.browserPrint.mode.landscape();
    map.printControl.print(printMode);
});

$(".leaflet-control-browser-print").css({
    display: "none",
});


// function to open up the pop up on draw end
var popup = L.popup({
    closeButton: true,
    autoClose: true,
    className: "custom-popup"
});


// var geoJsonData = $.ajax({
//     url: "json2.php",
//     dataType: "json",
//     type: "post",
//     data: $("#geoform").serialize();

// ajax: {
//     url: uri,
//     type: "POST",
//     data: { data: JSON.stringify(s) },
//     dataType: "json",
//     success: function(data, status) { .. }
// }

// $.ajax({
// type : "POST",
// url: "{% url 'ajax_posting' %}",
// data:$(this).serialize(),
// data: {
//  first_name : $('#first_name').val(),
//  last_name : $('#last_name').val(),
//  csrfmiddlewaretoken: '{{ csrf_token }}',
//  dataType: "json",
//
// },
//
// success: function(data){
//    $('#output').html(data.msg) /* response message */
// },
//
// failure: function() {
//
// }

function createFormPopup() {
    var popupContent =
        `<div class="form">
                <form action="{% url 'drawShape' %}" role="form" id="form" method="post" role="form" id="geoform" enctype="multipart/form-data">
                {% csrf_token %}
                    <h3 style="color: #15784e">Parcel Information</h3><hr>
                        <input type="text" name="lrnumber" id="lrnumber"  placeholder="LRN0/0001" required> <br><br>
                        <input type="number" name="plotno" id="plotno"  placeholder="Plot Number" required> <br><br>
                        <input type="hidden" name="polygon" id="polygon">
                    <input style="color: #ffffff" class="btn btn-primary btn-block" id='submit' type="submit" value="Submit">       
                </form>
            </div>`;

    editableLayers.bindPopup(popupContent).openPopup();
}

map.addEventListener("draw:created", function (e) {
    e.layer.addTo(editableLayers);

    var type = e.layerType,
        layer = e.layer;

    feature = layer.feature = layer.feature || {};
    feature.type = feature.type || "Feature";
    var props = feature.properties = feature.properties || {}; // initialize the feature property

    createFormPopup(); // opening the pop up

    if (type === "polygon") {
        // creating a geojson from the coordinates
        editableLayers.eachLayer(function (layer) {
            var area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);

            $("form").submit(function (e) {
                e.preventDefault();
                let parcelid = document.getElementById("lrnumber").value;
                let lrnumber = document.getElementById("plotno").value;
                let hidden_input = document.querySelector("[name='polygon']");
                hidden_input.value = JSON.stringify(layer.toGeoJSON().geometry);

                // adding more properties values to the geojson layer
                props.area = area;
                props.lrnumber = lrnumber;
                props.parcelid = parcelid;
                props.status = 'on sale';
                props.perimeter = 200;

                editableLayers.closePopup();
                // editableLayers.addLayer(layer); // adding the layer to the with properties

                // let data = JSON.stringify(editableLayers.toGeoJSON());
                data = JSON.stringify(editableLayers.toGeoJSON(), null, 4);
                $('#drawcontainer').html(data);
                console.log('serialized data', data)
                console.log('unserialized geojson', editableLayers.toGeoJSON());
                // console.log('hidden layer input', hidden_input.value);
                // console.log(typeof (hidden_input.value));
                // console.log('seridata', $(this).serialize());
                // console.log('layer to geojson', editableLayers.toGeoJSON(), null, 4);
                // console.log('serialized geometry', JSON.stringify(layer.toGeoJSON().geometry , null, 4));
            });

        });

    }
    ;


    if (type === "marker") {
        layer.bindPopup("LatLng: " + layer.getLatLng().lat + "," + layer.getLatLng().lng).openPopup();
        // editableLayers.addLayer(layer);
    }
});

// on click, clear all layers
document.getElementById('delete').onclick = function (e) {
    editableLayers.clearLayers();
    drawgeojson.clearLayers();
}


map.addEventListener("draw:editstart", function (e) {
    editableLayers.closePopup();
});

map.addEventListener("draw:deletestart", function (e) {
    editableLayers.closePopup();
});

map.addEventListener("draw:editstop", function (e) {
    // $(".drawercontainer .drawercontent").html(
    // JSON.stringify(editableLayers.toGeoJSON())
    // );
    editableLayers.openPopup();
});

map.addEventListener("draw:deletestop", function (e) {
    if (editableLayers.getLayers().length > 0) {
        editableLayers.openPopup();
    }
});

// map.on(L.Draw.Event.DELETED, function(e) {
//   $(".drawercontainer .drawercontent").html("");
// });


// Geoserver settings
var wms_Layer_url = "http://localhost:8080/geoserver/kenya/wms?";
var wfs_layer_url = "http://localhost:8080/geoserver/kenya/ows?"; //add  trailing question when using ajax
var getcaps = "http://localhost:8080/geoserver/kenya/wms?service=wms&version=1.3.0&request=GetCapabilities";
var attribution = "Map by Kevin Sambuli Amuhaya";

//Get WFS request from  geoserver
var wfsURL = wfs_layer_url + "service=wfs&version=1.0.0&request=GetFeature&typeName=kenya:counties&outputFormat=application/json";
console.log(wfsURL);

var counties = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'kenya:counties',
        format: 'image/png',
        tiled: true,
        transparent: true,
        attribution: attribution
    });

var population = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'population',
        format: 'image/png',
        transparent: true,
        tiled: true,
        opacity: 0.6,
        zIndex: 100,
        attribution: attribution
    });

var nairobiPlots = L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'nairobi',
        format: 'image/png',
        transparent: true,
        // tiled:true,
        opacity: 0.6,
        zIndex: 100,
        attribution: attribution
    }).addTo(map);

// control that shows state info on hover
var info = L.control({
    position: 'bottomright'
});
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>County</h4>' + (props ?
        '<b>' + props.countycode + '</b><br />' + props.countyname : 'Hover over a county');
};

info.addTo(map);


// Geojson style file
var myStyle = {
    stroke: true,
    fillColor: '#B04173',
    fillOpacity: 0.5,
    color: 'yellow ',
    weight: 1,
    Opacity: 1.0,
};

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: 'green',
        dashArray: 1,
        fillOpacity: 0.7,
        // fillCollor: "#c7e9c0pg"
        fillCollor: 'blue'
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    selectedArea.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}


// Geoserver Web Feature Service using Ajax
$.ajax(wfs_layer_url, {
    type: 'GET',
    data: {
        service: 'wfs',
        version: '1.0.0',
        request: 'GetFeature',
        typename: 'kenya:counties',
        maxFeatures: 50,
        srsname: 'EPSG:4326',
        outputFormat: 'text/javascript',
    },
    dataType: 'jsonp',
    jsonp: 'format_options',
    jsonpCallback: 'callback:handleJson',
    // jsonpCallback:'getJson',
    // success: handleJson,
    // beforeSend: function(s){
    // 		$('#result').html('tunggu');
    // 	},
    // error: function (xhr, status) {
    //       alert("Failed call Layer A");
    //   },
    //    headers: {
    //   'Access-Control-Allow-Credentials' : true,
    //   'Access-Control-Allow-Origin':'*',
    //   'Access-Control-Allow-Methods':'GET',
    //   'Access-Control-Allow-Headers':'application/json',
    // },
});

// console.log(map.getBounds().toBBoxString());
// console.log(map.getSize().x);
// console.log(map.getSize().y);


// the ajax callback function
function handleJson(data) {
    selectedArea = L.geoJson(data, {
        style: myStyle,
        onEachFeature: function onEachFeature(feature, layer) {
            var customOptions = {
                "maxWidth": "500px",
                "className": "customPop"
            };
            var popContent = "<div><b>" + "Code " + feature.properties.countycode + "</b></br>" + "Name "
                + feature.properties.countyname + "</div>";
            layer.bindPopup(popContent, customOptions);
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: zoomToFeature
            });
        }
    }).addTo(wfsLayer);
    map.fitBounds(selectedArea.getBounds());
}

// re order map z index
map.on("overLays", function (e) {
    wfsLayer.bringToBack();
    population.bringToBack();
    nairobiPlots.bringToFront();
    imgoverlay.bringToBack();
});


// var cqlFilter = "countyname='Nakuru'";
var defaultParameters = {
    service: 'wfs',
    version: '1.0.0',
    request: 'GetFeature',
    typeName: 'kenya:counties',
    // CQL_FILTER: cqlFilter,
    // cql_filter=INTERSECTS(the_geom,%20POINT(-105.36369323730467%2040.10013461308659))
    maxFeatures: 50,
    srsName: 'EPSG:4326',
    outputFormat: 'text/javascript',
};

//query string URL that automatically adds a question mark at the end of the string
// this applies when you use default parameters
var wfs_layer_url2 = "http://localhost:8080/geoserver/kenya/ows";
var parameters = L.Util.extend(defaultParameters);
var URL = wfs_layer_url2 + L.Util.getParamString(parameters);
console.log(URL);


// Geojson style file
var mySearchStyle = {
    stroke: true,
    fillColor: 'yellow',
    fillOpacity: 0.5,
    color: 'red',
    weight: 2,
    Opacity: 1.0,
};


// function that returns the searched layers
function searchWFS() {
    if (wfsLayerSearch != null) {
        map.removeLayer(wfsLayerSearch);
    }
    // get value from input inbox
    queryValue = document.getElementById("search-value").value;

    // cqlFilter = "countyname='" + queryValue + "'";
    cqlFilter = "countyname='" + queryValue + "' or " + "countyname LIKE '" + queryValue + "%'";
    // cqlFilter = "countyname LIKE'" + queryValue + "%'";
    // console.log(cqlFilter);
    // cql_filter=INTERSECTS(the_geom,%20POINT(-105.36369323730467%2040.10013461308659))

    geoLayer = 'counties';
    var typeName = "kenya:" + geoLayer;

    var defaultParameters = {
        service: 'wfs',
        version: '1.0.0',
        request: 'GetFeature',
        typeName: typeName,
        CQL_FILTER: cqlFilter,
        srsName: 'EPSG:4326',
        outputFormat: 'text/javascript',
    };

    var parameters = L.Util.extend(defaultParameters);
    var URL = wfs_layer_url2 + L.Util.getParamString(parameters);

    if (!queryValue) {
        $("#alert_empty").fadeTo(2000, 500).slideUp(500, function () {
            $(".alert").slideUp(500);
            alert("Please enter A valid Input!");
        });
    }

        // if (!queryValue) {
        //     alert("Please enter A valid Input!");
        //     return false;
    // }
    else {
        // alert("please wait");
        $.ajax(URL, {
            dataType: 'jsonp',
            jsonpCallback: 'callback:searchJson',
            jsonp: 'format_options'
        });
        return true;
    }
}

// the ajax callback function
function searchJson(data) {
    if (data.totalFeatures > 0) {
        document.getElementById("wfsResults").innerHTML = data.totalFeatures + " Total Results";

        wfsLayerSearch = L.geoJson(data, {
            style: mySearchStyle,
            onEachFeature: function onEachFeature(feature, layer) {
                layer.bindPopup("Code: " + feature.properties.countycode + "<br/>Name: " + feature.properties.countyname,
                    {
                        closeButton: false,
                        offset: L.point(0, -10)
                    });
                layer.on('mouseover', function () {
                    layer.openPopup();
                });
                layer.on('mouseout', function () {
                    layer.closePopup();
                });
            }
        }).addTo(map);
        // }).addTo(wfsLayerSearch);
        map.fitBounds(wfsLayerSearch.getBounds());
    } else {
        document.getElementById("wfsResults").innerHTML = "";
        $("#alert_noResult").fadeTo(2000, 500).slideUp(500, function () {
            $(".alert").slideUp(500);
        });
    }
}


//function to clear up results from clear button
function clearResult() {
    document.getElementById("search-value").value = "";
    document.getElementById("wfsResults").innerHTML = "";

    // Clear existing WFS Query Layer/Result
    if (wfsLayerSearch != null) {
        map.removeLayer(wfsLayerSearch);
    }
    // zoom to original extent
    map.setView(centerBounds, 6);
    return false;
}


//custom leaflet icon
var createIcon = function (labelText) {
    if (!labelText) {
        return L.divIcon({
            className: "textLabelClass",
        });
    }
    return L.divIcon({
        className: "textLabelClass",
        html: labelText
    });
};


//legend control function
function wmsLegendControl(layerName, layerTitle) {
    var className = layerName.split(":")[1];
    var url = `http://localhost:8080/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&LAYER=${layerName}`;
    var legend = `<p class="${className}" style='margion-top:10px; font-weight: bold'>${layerTitle}</p>`;
    legend += `<p><img class="${className}" src=${url} /><br class=${className} /></p> `;
    return legend;
}


L.Control.Watermark = L.Control.extend({
    onAdd: function (map) {
        var img = L.DomUtil.create('img');

        img.src = 'https://www.epix.net.pl/wp-content/uploads/2017/03/gis-logo.png';
        img.style.width = '200px';

        return img;
    },
    onRemove: function (map) {
        // Nothing to do here
    }
});

L.control.watermark = function (opts) {
    return new L.Control.Watermark(opts);
};

// var watermarkControl = L.control.watermark({position: 'bottomleft'}).addTo(map);


/*Legend specific*/
// var legend = L.control({ position: "bottomright" });
//
// legend.onAdd = function(map) {
//   var div = L.DomUtil.create("div", "legend");
//   div.innerHTML += "<h4>Tegnforklaring</h4>";
//   div.innerHTML += '<i style="background: #477AC2"></i><span>Water</span><br>';
//   div.innerHTML += '<i style="background: #448D40"></i><span>Forest</span><br>';
//   div.innerHTML += '<i style="background: #E6E696"></i><span>Land</span><br>';
//   div.innerHTML += '<i style="background: #E8E6E0"></i><span>Residential</span><br>';
//   div.innerHTML += '<i style="background: #FFFFFF"></i><span>Ice</span><br>';
//   div.innerHTML += '<i class="icon" style="background-image: url(https://d30y9cdsu7xlg0.cloudfront.net/png/194515-200.png);background-repeat: no-repeat;"></i><span>Grænse</span><br>';
//   return div;
// };
// legend.addTo(map);

// Create Leaflet Control Object for Legend
var legend = L.control({position: "bottomright"});

// Description contents
var contents = "";
contents += '<div id="description"><p><b>Simple shapes in Leaflet</b></p><hr>';
contents += '<p>This map shows an example of adding shapes on a Leaflet map<p/>';
contents += '<p>The following shapes were added:</p><br/>';
contents += '<p><ul>';
contents += '<li>A marker</li>';
contents += '<li>A line</li>';
contents += '<li>A polygon</li>';
contents += '</ul></p>';
contents += '<p>The line layer has a <b>popup</b>. Click on the line to see it!</p><hr>';
contents += '<p>Created with the Leaflet library</p><br/>';
contents += '<img src="./image/map.jpg"></div>';


// Function that runs when legend is added to map
legend.onAdd = function (map) {

    // Create Div Element and Populate it with HTML
    div = L.DomUtil.create('div', 'legend');
    div.innerHTML = contents;
    div.innerHTML += '<input type="button" value="hide" id="hide">';

    // Return the Legend div containing the HTML content
    return div;

};

// Add Legend to Map
// legend.addTo(map);


//Handle Map click to Display Lat/Lng
// map.on('click', function(e) {
//   $("#latlng").html(e.latlng.lat + ", " + e.latlng.lng);
// 	$("#latlng").show();
// });

//Handle Copy Lat/Lng to clipboard
$('#latlng').click(function (e) {
    var $tempElement = $("<input>");
    $("body").append($tempElement);
    $tempElement.val($("#latlng").text()).select();
    document.execCommand("Copy");
    $tempElement.remove();
    alert("Copied: " + $("#latlng").text());
    $("#latlng").hide();
});


// 'Hide' button that toggles the legend
$("#hide").on("click", function () {
    L.DomEvent.disableClickPropagation(this);
    switch ($("#hide").val()) {
        case "hide":
            $("#description").slideUp();
            $("#hide").val("show");
            break;
        case "show":
            $("#description").slideDown();
            $("#hide").val("hide");
            break;
    }
});


// map overlays
var overLays = {
    "Georeferenced": imgoverlay,
    "Nairobi": nairobiPlots,
    "County (WMS)": counties,
    "Population  (WMS)": population,
    "wfsLayer (WFS)": wfsLayer,
    "Search": wfsLayerSearch,
    "Draw": editableLayers,
    "DrawGeojson": drawgeojson,

};


// Show coordinates
// var div = document.createElement('div');
// div.id = 'coordsDiv';
// div.style.position = 'absolute';
// div.style.bottom = '0';
// div.style.left = '0';
// div.style.zIndex = '999';
// document.getElementById('map').appendChild(div);
//
// map.on('mousemove', function(e) {
//
//   var lat = e.latlng.lat.toFixed(5);
//   var lon = e.latlng.lng.toFixed(5);
//
//   document.getElementById('coordsDiv').innerHTML = lat + ', ' + lon;
//
// });

// adding the map layers to layer control
// var layers=  L.control.layers(basemaps, overLays, {collapsed: true, position: 'topright'});
// layers.addBaseLayer(imgoverlay, 'Georeference').addTo(map);

L.control.layers(basemaps, overLays, {collapsed: true, position: 'topright'}).addTo(map);