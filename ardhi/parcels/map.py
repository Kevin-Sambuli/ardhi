import folium, branca
from folium import plugins, raster_layers, vector_layers
from branca.element import Figure
from folium.features import GeoJsonPopup, GeoJsonTooltip
import os


def color_producer(perimeter):
    if perimeter < 185:
        return 'green'
    elif 185 <= perimeter < 200:
        return 'orange'
    else:
        return 'red'


def my_map(land_parcels, parcel=None, lat=None, lng=None):
    extent = [-1.22488, 36.82467]
    m = folium.Map(location=extent, min_zoom=8, zoom_start=15,
                   max_zoom=18, control_scale=True, tiles="OpenStreetMap")
    # map0 = raster_layers.TileLayer(tiles='OpenStreetMap', name='OSM').add_to(m)
    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter', name='Dark').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron', name='CartoBD').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain', name='Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner', name='Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor', name='Watercolor').add_to(m)

    # m.choropleth(
    #     geo_data=land_parcels,
    #     name='Maps',
    #     key_on='feature.id',
    #     fill_color='green',
    #     fill_opacity='0.2',
    #     line_opacity='2',
    #     legend_name='Land parcels',
    #     tooltip='No Access to this information'
    # )
    # dictionary that holds the style of our selected parcel shapefile
    style_parcel = {'fillcolor': '#228822', 'color': '#228822'}

    m.add_child(folium.LatLngPopup())
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.LocateControl().add_to(m)

    popup = GeoJsonPopup(
        fields=["pk", "owner", "area_ha", "perimeter", "status", "lr_no"],
        aliases=["Parcel id :", "Owner id :", "Area (ha):", "Perimeter(m):", "Status:", "LR No:"],
        localize=True, labels=True,
        style="background-color: green;",
        )

    parc = folium.features.GeoJson(land_parcels, name='Map', highlight_function=None, zoom_on_click=True,
                                   control=True, popup=popup, overlay=True, show=True, smooth_factor=None,
                                   embed=True, ).add_to(m)

    folium.plugins.Search(layer=parc, geom_type="Polygon", zoom_on_click=True, placeholder="Search for parcel",
                          collapsed=False, search_zoom=18, search_label="lr_no", weight=3, ).add_to(m)
    if parcel:
        folium.features.GeoJson(parcel, style_function=lambda x: style_parcel, highlight_function=None, name='Parcels',
                                overlay=True, control=True, popup=parcel, show=True, smooth_factor=None,
                                tooltip='my parcel', embed=True).add_to(m)


    # myIcon = L.divIcon({iconUrl: 'my-ion.png'})
    img = folium.features.DivIcon(html="<div> <img src='img.jpg' width='500' height='600'></div>",
                            icon_size=None, icon_anchor=None, popup_anchor=None, class_name='empty')

    if lat and lng:
        folium.Marker([lat, lng], icon=folium.Icon(color="red", icon="info-sign"), tooltip='Click for more',
                      popup='parcels', ).add_to(m)

    folium.plugins.MeasureControl(position='topleft', primary_length_unit='meters', secondary_length_unit='miles',
                                  primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)

    folium.LayerControl(position="topright", strings={"title": "my location", "popup": "Your position"}).add_to(m)
    folium.plugins.Geocoder(collapsed=True, position='topright', add_marker=True, ).add_to(m)

    folium.plugins.MousePosition(separator=':', empty_string='Unavailable', lng_first=False, num_digits=5, ).add_to(m)

    folium.plugins.MiniMap(tile_layer='CartoDB Dark_Matter', position='bottomright', width=120, height=120,
                           collapsed_width=25, collapsed_height=25, zoom_level_offset=-5, zoom_level_fixed=None,
                           center_fixed=False, zoom_animation=False, toggle_display=True,
                           auto_toggle_display=False, minimized=True, ).add_to(m)

    # folium.raster_layers.WmsTileLayer(
    #     url="http://localhost:8600/geoserver/wms/",
    #     name="counties",
    #     fmt="image/png",
    #     layers="counties",
    #     attr=u"Kevin Sambuli",
    #     transparent=True,
    #     overlay=True,
    #     control=True,
    # ).add_to(m)

    # merc = os.path.join("parcels", "map.jpg")
    # img = "parcels/map.jpg"

    # folium.raster_layers.ImageOverlay(name="map",
    #                                   image=merc,
    #                                   bounds=[[-1.22149772193, 36.8221708365], [-1.22929592861, 36.8277197066]],
    #                                   ).add_to(m)

    # img.add_to(m)
    # folium.LayerControl().add_to(m)

    return m
