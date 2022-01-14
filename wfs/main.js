
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

// $('.leaflet-prevent').on('click', L.DomEvent.stopPropagation);
//  var pinToggler = True;

// $('.pin').on('click', function () {
//    if(pinToggler){
//    }
// })

//function to fire up wfs keyword search
var queryValue = null;
var geoLayer = null;
var cqlFilter = null;
var selectedArea = null;
var area = null;
// var wfsLayerSearch;



//Init BaseMaps
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

// map options
var lat =  -1.22488;
var lng =  36.827164;

//Map Options
var mapOptions = {
  zoomControl: false,
  attributionControl: false,
  center: [lat, lng],
  zoom: 6.2,
  layers: [basemaps.Dark]
};

//create the map object
let map = L.map('map' , mapOptions);
// map.zoomControl.setPosition('topleft');

// Get Map's Center
var centerBounds = map.getBounds().getCenter();

// scale control layer
L.control.scale({metric:true, imperial:false, maxWidth:100}).addTo(map);

//Render Zoom Control
L.control.zoom({position: "topleft"}).addTo(map);

//zoom to extent button
$(".default-view").on("click", function () {
    map.fitBounds(selectedArea.getBounds());
});

//mouse hover coordinates
map.on("mousemove", function(e){
    $(".map-coordinate").html("Lat : " + e.latlng.lat + " Lng : " +e.latlng.lng);
});



var wfsLayer = new L.featureGroup();
var wfsLayerSearch = new L.featureGroup();
var editableLayers = new L.FeatureGroup().addTo(map);
map.addLayer(editableLayers);


// var sidebar = L.control
//   .sidebar({
//     autopan: false,
//     container: "sidebar",
//     position: "right"
//   })
//   .addTo(map);

// // Render Layer Control & Move to Sidebar
// var layerControl = L.control
//   .layers(basemaps, overLays, {
//     position: "topright",
//     collapsed: false
//   })
//   .addTo(map);

// var oldLayerControl = layerControl.getContainer();
// var newLayerControl = $("#layercontrol");
// newLayerControl.append(oldLayerControl);
// $(".leaflet-control-layers-list").prepend("<strong class='title'>Base Maps</strong><br>");
// $(".leaflet-control-layers-separator").after("<br><strong class='title'>Layers</strong>");



var MyCustomMarker = L.Icon.extend({
        options: {
            shadowUrl: null,
            iconAnchor: new L.Point(12, 12),
            iconSize: new L.Point(24, 24),
            iconUrl: 'image/logo.png'
        }
});

var drawOptions = {
  position: "bottomleft",
  draw: {
    polyline:  {
        shapeOptions: {
            color: '#f357a1',
            weight: 10,
        }
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
      allowIntersection: true, // Restricts shapes to simple polygons
      showArea:true,
      metric: false,
      repeatMode: false,
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
      drawError: {
        color: "#e1e100", // Color the shape will turn when intersects
        message: "<strong>Oh snap!<strong> you can't draw that!" // Message that will show when intersect
      }
    }
  },

  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: true
    // remove: false
  }
};

var drawControl = new L.Control.Draw(drawOptions);
map.addControl(drawControl);

// function to open up the pop up on draw end
var popup = L.popup({
  closeButton: true,
  autoClose: true,
  className: "custom-popup"
});


function createFormPopup() {
    let popupContent =
        '<form action="/"  method="post" role="form" id="form" enctype="multipart/form-data">' +
            '<h3 style="color: #15784e">Parcel Information</h3><hr>' +
            'Parcel Number:<br><br>' +
                '<input type="number" id="parcelId" name="parcelId" placeholder="Parcel  ID" required><br><br>' +
                '<small></small>'+
            'LRNumber:<br><br>' +
                '<input type="text" id="lrNumber" name="lrNumber" placeholder="Parcel Number" required><br><br><hr>' +
                '<small></small>'+
                '<input type="hidden" name="polygon">'+
                '<input style="color: #ffffff" class="btn btn-primary btn-block" type="submit" value="Submit">' +
        '</form>';
    var popupOptions =
        {
          'maxWidth': '200',
          'className' : 'another-popup'
        };
    editableLayers.bindPopup(popupContent).openPopup();
    // editableLayers.bindPopup(popupContent, popupOptions).openPopup();
}


// document.querySelector("form").addEventListener("submit", function(e){
//   e.preventDefault();
//
//   // Stringify the object and store it in the hidden input
//     // Get user name and description
//     let parcelid = document.getElementById("parcelId").value;
//     let lrnumber = document.getElementById("lrNumber").value;
//     let hidden_input = document.querySelector("[name='polygon']");
//     hidden_input.value = JSON.stringify(layer.toGeoJSON().geometry);
//
//     console.log(hidden_input.value);
//     console.log(typeof(hidden_input.value));
// });


// The setData function collects all of the user entered information into three variables
function setData(e) {
    if(e.target && e.target.id == "submit") {

        // Get user name and description
        let enteredUsername = document.getElementById("parcelId").value;
        let enteredDescription = document.getElementById("lrnumber").value;

        // Print user name and description
        console.log(enteredUsername);
        console.log(enteredDescription);

        // Get and print GeoJSON for each drawn layer
        editableLayers.eachLayer(function(layer) {
            let drawing = JSON.stringify(layer.toGeoJSON().geometry);
            console.log(drawing);
        });

        // Clear drawn items layer
        editableLayers.closePopup();
        editableLayers.clearLayers();

    }

}

// document.addEventListener("click", setData);

map.addEventListener("draw:created", function(e) {
// map.on(L.Draw.Event.CREATED, function(e) {
    var coordinates = [];
    console.log('cordinates', coordinates);

    var type = e.layerType,
    layer = e.layer;

    if (type === "polygon") {
        editableLayers.addLayer(layer);
        // creating a geojson from the coordinates
        editableLayers.eachLayer(function (layer){
            feature = layer.feature = layer.feature || {};
            feature.type = feature.type || "Feature";

            var area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
            // console.log('area', area);
            // e.layer.bindPopup((LGeo.area(e.layer) / 1000000).toFixed(2) + ' km<sup>2</sup>');

            var props = feature.properties = feature.properties || {};
            props.area = area;
            props.lrnumber = null;
            props.status = null;
            props.perimeter = 200;

            let data = JSON.stringify(editableLayers.toGeoJSON());
            $('#results').html(data);

            console.log(editableLayers.toGeoJSON());

            // let geojson = JSON.stringify(editableLayers.toGeoJSON());
            //     // console.log(geojson);
            let geojson2 = JSON.stringify(layer.toGeoJSON().geometry);
            //  let geojson3= JSON.stringify(layer.toGeoJSON());
            //     console.log(geojson2);

            createFormPopup(); // opening up the pop up

            $("form").submit(function (e) {
                e.preventDefault();
                let parcelid = document.getElementById("parcelId").value;
                let lrnumber = document.getElementById("lrNumber").value;
                let hidden_input = document.querySelector("[name='polygon']");
                hidden_input.value = JSON.stringify(layer.toGeoJSON().geometry);

                console.log(hidden_input.value);
                console.log(typeof(hidden_input.value));

                editableLayers.closePopup();

            });


        });

        // console.log("my array: ",layer.getLatLngs()[0]);

        var latlngs = layer.getLatLngs()[0];
        // editableLayers.addLayer(layer);


        for (var i = 0; i < latlngs.length; i++) {
            coordinates.push([latlngs[i].lng, latlngs[i].lat])
        }
    }

    if (type === "marker") {
        layer.bindPopup("LatLng: " + layer.getLatLng().lat + "," + layer.getLatLng().lng).openPopup();
    }
    editableLayers.addLayer(layer);

    // layer.on("click", function (e) {
    //     console.log("layer click");
    //     console.log(e);
    // });

    // layer.on("touchstart", function (e) {
    //     console.log("layer touchstart");
    //     console.log(e);
    // });

    // editableLayers.on("click", function (e) {
    //     console.log("editableLayers2 click");
    //     console.log(e);
    // });

    // editableLayers.on("touchstart", function (e) {
    //     console.log("editableLayers2 touchstart");
    //     console.log(e);
    // });
});

// $("form").submit(function (e) {
//         // preventing from page reload and default actions
//         e.preventDefault();
//         // serialize the data for sending the form data.
//         var serializedData = $(this).serialize();
//         // make POST ajax call
//         $.ajax({
//             type: 'POST',
//             url: "{% url 'post_friend' %}",
//             data: serializedData,
            // success: function (response) {
            //     // on successfull creating object
            //     // 1. clear the form.
            //     $("#friend-form").trigger('reset');
            //     // 2. focus to nickname input
            //     $("#id_nick_name").focus();
            //
            //     // display the newly friend to table.
            //     var instance = JSON.parse(response["instance"]);
            //     var fields = instance[0]["fields"];
            //     $("#my_friends tbody").prepend(
            //         `<tr>
            //         <td>${fields["nick_name"]||""}</td>
            //         <td>${fields["first_name"]||""}</td>
            //         <td>${fields["last_name"]||""}</td>
            //         <td>${fields["likes"]||""}</td>
            //         <td>${fields["dob"]||""}</td>
            //         <td>${fields["lives_in"]||""}</td>
            //         </tr>`
            //     )
            // },
    //         error: function (response) {
    //             // alert the error if any error occured
    //             alert(response["responseJSON"]["error"]);
    //         }
    //     })
    // })

map.addEventListener("draw:editstart", function(e) {
    editableLayers.closePopup();
});

map.addEventListener("draw:deletestart", function(e) {
    editableLayers.closePopup();
});

// map.on(L.Draw.Event.EDITSTOP, function(e) {
map.addEventListener("draw:editstop", function(e) {
    // $(".drawercontainer .drawercontent").html(
    // JSON.stringify(editableLayers.toGeoJSON())
   // );
    editableLayers.openPopup();
});

// map.on(L.Draw.Event.DELETED, function(e) {
map.addEventListener("draw:deletestop", function(e) {
    if(editableLayers.getLayers().length > 0) {
        editableLayers.openPopup();
    }
});


// $(".drawcontainer").html(JSON.stringify(editableLayers.toGeoJSON()));

// map.on(L.Draw.Event.EDITSTOP, function(e) {
//   $(".drawercontainer .drawercontent").html(
//     JSON.stringify(editableLayers.toGeoJSON())
//   );
// });
//
// map.on(L.Draw.Event.DELETED, function(e) {
//   $(".drawercontainer .drawercontent").html("");
// });

// //Edit Button Clicked
// $('#toggledraw').click(function(e) {
//   $(".leaflet-draw").fadeToggle("fast", "linear");
//   map.addControl(drawControl);
//   $(".leaflet-draw-toolbar").fadeToggle("fast", "linear");
//   this.blur();
//   return false;
// });

// //Handle Map click to Display Lat/Lng
// map.on('click', function(e) {
//   $("#latlng").html(e.latlng.lat + ", " + e.latlng.lng);
// 	$("#latlng").show();
// });

// //Handle Copy Lat/Lng to clipboard
// $('#latlng').click(function(e) {
//   var $tempElement = $("<input>");
// 	$("body").append($tempElement);
// 	$tempElement.val($("#latlng").text()).select();
// 	document.execCommand("Copy");
// 	$tempElement.remove();
// 	alert("Copied: "+$("#latlng").text());
// 	$("#latlng").hide();
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
        tiled:true,
        transparent: true,
        attribution: attribution
    });

var population= L.tileLayer.wms("http://localhost:8080/geoserver/wms",
    {
        layers: 'population',
        format: 'image/png',
        transparent: true,
        tiled:true,
        opacity:0.6,
        zIndex:100,
        attribution: attribution
    });


// control that shows state info on hover
var info = L.control();
info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>County</h4>' +  (props ?
        '<b>' + props.countycode + '</b><br />' + props.countyname : 'Hover over a county');
};

info.addTo(map);


//legend control function
function wmsLegendControl(layerName, layerTitle) {
  var className = layerName.split(":")[1];
  var url = `http://localhost:8080/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&LAYER=${layerName}`;
  var legend = `<p class="${className}" style='margion-top:10px; font-weight: bold'>${layerTitle}</p>`;
  legend += `<p><img class="${className}" src=${url} /><br class=${className} /></p> `;
  return legend;
}



// L.Control.Watermark = L.Control.extend({
// 		onAdd: function (map) {
// 			var img = L.DomUtil.create('img');
//
// 			img.src = 'https://www.epix.net.pl/wp-content/uploads/2017/03/gis-logo.png';
// 			img.style.width = '200px';
//
// 			return img;
// 		},
// 		onRemove: function (map) {
// 			// Nothing to do here
// 		}
// 	});
//
// L.control.watermark = function (opts) {
// 		return new L.Control.Watermark(opts);
// 	};
//
// var watermarkControl = L.control.watermark({position: 'bottomleft'}).addTo(map);


 // Geojson style file
var myStyle = {
    stroke: true,
    fillColor: '#B04173',
    fillOpacity: 0.5,
    color: 'yellow ',
    weight: 1,
    Opacity:1.0,
};

function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: 'green',
			dashArray: 1,
			fillOpacity: 0.7,
			fillCollor: "#c7e9c0pg"
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
$.ajax(wfs_layer_url,{
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
  jsonpCallback:'callback:handleJson',
  jsonp:'format_options'
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
            "maxWidth":"500px",
            "className":"customPop"
        };
        var popContent ="<div><b>" + "Code " + feature.properties.countycode + "</b></br>" + "Name "
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
    srsName:'EPSG:4326',
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
    Opacity:1.0,
};


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

    geoLayer = 'counties';
    var typeName = "kenya:" + geoLayer;

    var defaultParameters = {
        service: 'wfs',
        version: '1.0.0',
        request: 'GetFeature',
        typeName: typeName,
        CQL_FILTER: cqlFilter,
        srsName:'EPSG:4326',
        outputFormat: 'text/javascript',
    };

    var parameters = L.Util.extend(defaultParameters);
    var URL = wfs_layer_url2 + L.Util.getParamString(parameters);

    if (!queryValue) {
        $("#alert_empty").fadeTo(2000,500).slideUp(500, function(){
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
            jsonpCallback:'callback:searchJson',
            jsonp:'format_options'
        });
        return true;
    }
}

// the ajax callback function
function searchJson(data) {
    if (data.totalFeatures > 0) {
        document.getElementById("wfsResults").innerHTML=data.totalFeatures + " Total Results";

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
        $("#alert_noResult").fadeTo(2000,500).slideUp(500, function(){
           $(".alert").slideUp(500);
            });
        }
}


//function to clear up results from clear button
function clearResult()   {
     document.getElementById("search-value").value = "";
     document.getElementById("wfsResults").innerHTML="";

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
    if(!labelText) {
        return L.divIcon({
        className: "textLabelClass",
        });
    }
    return L.divIcon({
        className: "textLabelClass",
        html: labelText
    });
};

/*Legend specific*/
var legend = L.control({ position: "bottomright" });

legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += "<h4>Tegnforklaring</h4>";
  div.innerHTML += '<i style="background: #477AC2"></i><span>Water</span><br>';
  div.innerHTML += '<i style="background: #448D40"></i><span>Forest</span><br>';
  div.innerHTML += '<i style="background: #E6E696"></i><span>Land</span><br>';
  div.innerHTML += '<i style="background: #E8E6E0"></i><span>Residential</span><br>';
  div.innerHTML += '<i style="background: #FFFFFF"></i><span>Ice</span><br>';
  div.innerHTML += '<i class="icon" style="background-image: url(https://d30y9cdsu7xlg0.cloudfront.net/png/194515-200.png);background-repeat: no-repeat;"></i><span>Grænse</span><br>';
  return div;
};
// legend.addTo(map);




// map overlays
var overLays = {
    "County (WMS)": counties,
    "Population  (WMS)": population,
    "wfsLayer (WFS)": wfsLayer,
    "Search": wfsLayerSearch,
    // "Draw": editableLayers,
};

// adding the map layers to layer control
L.control.layers(basemaps, overLays, {collapsed: true, position: 'topright'}).addTo(map);