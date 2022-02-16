
var editableLayers = new L.FeatureGroup();
var layerEditable = new L.FeatureGroup();

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


var options = {
  position: 'topleft',
  drawMarker: true,
  drawPolygon: true,
  drawPolyline: true,
  drawCircle: true,
  editPolygon: true,
  deleteLayer: true
};

// add leaflet.pm controls to the map
map.pm.addControls(options);

// const shapes = [{
//     "type": "Feature",
//     "properties": {},
//     "geometry": {
//     "type": "Polygon",
//     "coordinates": [
//       [
//         [-3.701856, 40.422481],
//         [-3.707092, 40.418593],
//         [-3.70177, 40.417809],
//         [-3.701899, 40.422873],
//         [-3.701856, 40.422481]
//       ]
//     ]
//     }
//     }];
// const geojson = L.geoJSON(shapes).addTo(map);
//
// map.on('pm:remove', payload => {
//     const shapes = [];
//
//     map.eachLayer((layer) => {
//     if (layer.pm) {
//       const geojson = layer.toGeoJSON();
//
//       if (layer instanceof L.Circle) {
//         geojson.properties.radius = 10;
//       }
//
//       shapes.push(geojson);
//     }
//     });
//
// console.log('pm:remove');
// console.log(shapes);
// });

// map.on('pm:create', payload => {
// 	 	  const shapes = [];
//
// 	 	  map.eachLayer((layer) => {
// 	 	    if (layer.pm) {
// 	 	      const geojson = layer.toGeoJSON();
//
// 	 	      if (layer instanceof L.Circle) {
// 	 	        geojson.properties.radius = 10;
// 	 	      }
//
// 	 	      shapes.push(geojson);
// 	 	    }
// 	 	  });
//
// 	 	  console.log('pm:remove');
// 	 	  console.log(shapes);
// 	 	});


// L.Control.Command = L.Control.extend({
//     options: {
//         position: 'topleft',
//     },
//
//     onAdd: function (map) {
//         var controlDiv = L.DomUtil.create('div', 'leaflet-control-command');
//         L.DomEvent
//             .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
//             .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
//         .addListener(controlDiv, 'click', function () { MapShowCommand(); });
//
//         var controlUI = L.DomUtil.create('div', 'leaflet-control-command-interior', controlDiv);
//         controlUI.title = 'Map Commands';
//         return controlDiv;
//     }
// });
//
// L.control.command = function (options) {
//     return new L.Control.Command(options);
// };


// L.Control.RemoveAll = L.Control.extend(
// {
//     options:
//     {
//         position: 'topleft',
//     },
//     onAdd: function (map) {
//         var controlDiv = L.DomUtil.create('div', 'leaflet-draw-toolbar leaflet-bar');
//         L.DomEvent
//             .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
//             .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
//         .addListener(controlDiv, 'click', function () {
//             drawnItems.clearLayers();
//         });
//
//         var controlUI = L.DomUtil.create('a', 'leaflet-draw-edit-remove', controlDiv);
//         controlUI.title = 'Remove All Polygons';
//         controlUI.href = '#';
//         return controlDiv;
//     }
// });
// var removeAllControl = new L.Control.RemoveAll();
// map.addControl(removeAllControl);






// map.on(L.Draw.Event.CREATED, function (e) {
//   console.clear();
//   var type = e.layerType
//   var layer = e.layer;
//
//
//   // Do whatever else you need to. (save to db, add to map etc)
//
//   drawnItems.addLayer(layer);
//
//   console.log("Coordinates:");
//
//   if (type == "marker" || type == "circle" || type == "circlemarker"){
//     console.log([layer.getLatLng().lat, layer.getLatLng().lng]);
//   }
//   else {
//     var objects = layer.getLatLngs()[0];
//     for (var i = 0; i < objects.length; i++){
//       console.log([objects[i].lat,objects[i].lng]);
//     }
//   }
//
//
// });
