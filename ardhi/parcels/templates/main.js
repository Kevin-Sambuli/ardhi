
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
// var pinToggler = true;
//
// $('.pin').on('click', function () {
//    if(pinToggler){
//        map.on('click', function(e){
//         var lat = e.latlng.lat;
//         var lng = e.latlng.lng;
//         var marker = L.marker([e.latlng.lat, e.latlng.lng]).bindPopup('popup');
//         marker.addTo(map)
//     })
//     pinToggler = !pinToggler;
//     }else {
//         map.off('click')
//     }
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

var sidebar = L.control
  .sidebar({
    autopan: true,
    container: "sidebar",
    position: "right"
  })
  .addTo(map);



var wfsLayer = new L.featureGroup();
var drawgeojson = new L.featureGroup();
var wfsLayerSearch = new L.featureGroup();
var editableLayers = new L.FeatureGroup().addTo(map);
map.addLayer(editableLayers);

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
        metric: false,
        repeatMode: false,
    }
  },

  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: true,
    poly : {
      allowIntersection : false
    }
  }
};


$('.leaflet-prevent').on('click', L.DomEvent.stopPropagation);
var pinToggler = true;

// $('.pin').on('click', function () {
//    if(pinToggler){
//        var drawOptions = {
//   position: "bottomleft",
//   draw: {
//     polyline:  {
//         shapeOptions: {
//             color: '#f357a1',
//             weight: 10,
//         }
//     },
//     // circle: true, // Turns off this drawing tool
//     // rectangle: false,
//     rectangle: {
//         shapeOptions: {
//             clickable: false
//         }
//     },
//     marker: true,
//     // marker: {icon: new MyCustomMarker()}
//
//     polygon: {
//         shapeOptions: {
//             stroke:true,
//             color: '#f357a1',
//             weight: 10,
//             lineCap:'round',
//             lineJoin:'round',
//             opacity: 0.5,
//             fill: true,
//             fillColor: null,
//             fillOpacity: 0.2,
//             clickable: true
//       },
//       allowIntersection: false, // Restricts shapes to simple polygons
//       drawError: {
//         color: "#e1e100", // Color the shape will turn when intersects
//         message: "<strong>Oh snap!<strong> you can't draw that!" // Message that will show when intersect
//       },
//         showArea:true,
//         metric: false,
//         repeatMode: false,
//     }
//   },
//
//   edit: {
//     featureGroup: editableLayers, //REQUIRED!!
//     remove: true,
//     poly : {
//       allowIntersection : false
//     }
//   }
// };
//        map.on('click', function(e){
//         var drawControl = new L.Control.Draw(drawOptions);
//             map.addControl(drawControl);
//     })
//     pinToggler = !pinToggler;
//     } else {
//        map.removeControl(drawControl);
//         map.off('click')}
//     }
// })


var drawControl = new L.Control.Draw(drawOptions);
// map.removeControl(drawControl);
map.addControl(drawControl);

//Edit Button Clicked
$('#pin').click(function(e) {
    map.addControl(drawControl);
  $(".leaflet-draw").fadeToggle("fast", "linear");
  $(".leaflet-draw-toolbar").fadeToggle("fast", "linear");
  // this.blur();
  return true;
});


// var drawControl = new L.Control.Draw(drawOptions);
// map.addControl(drawControl);

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
    var popupContent = `<div class="form">
                <form action="/" role="form" id="form" method="post" role="form" id="geoform" enctype="multipart/form-data">
<!--                {% csrf_token %}-->
                    <h3 style="color: #15784e">Parcel Information</h3><hr>
<!--                    <div class="form-group">
                       <label>Title</label>-->
                            <input type="number" name="parcelid" id="parcelId"  placeholder="Parcel Id" required> <br><br>
<!--                    </div>-->
                    <input type="number" name="lrnumber" id="lrnumber"  placeholder="Parcel Number" required> <br><br><hr>
                    <input type="hidden" name="polygon" id="polygon">
<!--                    <input type="hidden" name="lat" value="${lat}">-->
                    <input style="color: #ffffff" class="btn btn-primary btn-block" id='submit' type="submit" value="Submit">       
                </form>
            </div>`;

    editableLayers.bindPopup(popupContent).openPopup();
}


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
        // editableLayers.clearLayers();

    }

}

// document.addEventListener("click", setData);


map.addEventListener("draw:created", function(e) {

    var type = e.layerType,
    layer = e.layer;
    var data =null;
    // var DrawGeoJSON = null;
    // var cities = L.layerGroup().addLayer(editableLayers).addTo(map);

    if (type === "polygon") {
        e.layer.addTo(editableLayers);

        // creating a geojson from the coordinates
        editableLayers.eachLayer(function (layer) {
            var area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
            console.log('area', area / 1000000);

            feature = layer.feature = layer.feature || {};
            feature.type = feature.type || "Feature";
            var props = feature.properties = feature.properties || {}; // initialize the feature property

            createFormPopup(); // opening up the popup form for every drawn item

            //  $(document).on('click','.submit',function(){
            //     $( "#form" ).submit();
            // });

            $("form").submit(function (e) {
                e.preventDefault();
                let parcelid = document.getElementById("parcelId").value;
                let lrnumber = document.getElementById("lrnumber").value;
                let hidden_input = document.querySelector("[name='polygon']");
                hidden_input.value = JSON.stringify(layer.toGeoJSON().geometry);

                // adding more properties values to the geojson layer
                // props.area = '1234';
                props.area = area;
                props.lrnumber = lrnumber;
                props.parcelid = parcelid;
                props.status = 'on sale';
                props.perimeter = 200;

                editableLayers.closePopup();
                // editableLayers.addLayer(layer);

                // let data = JSON.stringify(editableLayers.toGeoJSON());
                data = JSON.stringify(editableLayers.toGeoJSON(), null, 4);

                // console.log('hidden layer input', hidden_input.value);
                // console.log(typeof (hidden_input.value));
                // console.log('seridata', $(this).serialize());
                console.log('serialized data', data);
                // console.log('layer to geojson', editableLayers.toGeoJSON(), null, 4);
                // console.log('serialized geometry', JSON.stringify(layer.toGeoJSON().geometry , null, 4));
                $('#results').html(data);
                console.log('geojson', editableLayers.toGeoJSON());

                // function onEachFeature(feature, layer) {
                //     // does this feature have a property named popupContent?
                //     if (feature.properties && feature.properties.lrnumber ){
                //         layer.bindPopup(feature.properties.lrnumber);
                //     }
                // }
                // var DrawGeoJSON = L.geoJson(editableLayers.toGeoJSON(), {
                //     onEachFeature: onEachFeature}).addTo(drawgeojson);

            });

        });

    };
    // make POST ajax call
    //     $.ajax({
    //         type: 'POST',
    //         // url: "{% url 'post_parcels' %}",
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


    if (type === "marker") {
        layer.bindPopup("LatLng: " + layer.getLatLng().lat + "," + layer.getLatLng().lng).openPopup();
         // editableLayers.addLayer(layer);
    }

});

map.addEventListener("draw:editstart", function(e) {
    editableLayers.closePopup();
});

map.addEventListener("draw:deletestart", function(e) {
    editableLayers.closePopup();
});

map.addEventListener("draw:editstop", function(e) {
    // $(".drawercontainer .drawercontent").html(
    // JSON.stringify(editableLayers.toGeoJSON())
   // );
    editableLayers.openPopup();
});

map.addEventListener("draw:deletestop", function(e) {
    if(editableLayers.getLayers().length > 0) {
        editableLayers.openPopup();
    }
});

// map.on(L.Draw.Event.DELETED, function(e) {
//   $(".drawercontainer .drawercontent").html("");
// });


// //Edit Button Clicked
// var drawControl = new L.Control.Draw(drawOptions);
// map.addControl(drawControl);
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
  jsonp:'format_options',
  jsonpCallback:'callback:handleJson',
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


// function handleAjax(column, value, adminUnit = "AFG_adm2") {
//   $.ajax("https://lrimsfaoaf.ait.ac.th/geoserver/wfs", {
//     type: "GET",
//     data: {
//       service: "WFS",
//       version: "1.1.0",
//       request: "GetFeature",
//       typename: `geonode:${adminUnit}`,
//       CQL_FILTER: `${column}='${value}'`,
//       srsname: "EPSG:4326",
//       outputFormat: "text/javascript",
//     },
//     dataType: "jsonp",
//     jsonpCallback: "callback:handleJson",
//     jsonp: "format_options",
//   });
// }

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
    "Draw": editableLayers,
    "DrawGeojson": drawgeojson,
};

// adding the map layers to layer control
L.control.layers(basemaps, overLays, {collapsed: false, position: 'topright'}).addTo(map);