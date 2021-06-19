import folium
from folium import plugins, raster_layers


def color_producer(perimeter):
    if perimeter < 185:
        return 'green'
    elif 185 <= perimeter < 200:
        return 'orange'
    else:
        return 'red'


def my_map(land_parcels, parcel):
    extent = [-1.22488, 36.82467]
    m = folium.Map(location=extent, min_zoom=16, zoom_start=17, max_zoom=18, control_scale=True, tiles="CartoDB Dark_Matter", )
    map0 = raster_layers.TileLayer(tiles='OpenStreetMap', name='OSM', min_zoom=16, zoom_start=17, max_zoom=18).add_to(m)
    # map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter', name='Dark').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron', min_zoom=16, zoom_start=17, max_zoom=18, name='CartoBD').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain', min_zoom=16, zoom_start=17, max_zoom=18, name='Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner', min_zoom=16, zoom_start=17, max_zoom=18, name='Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor', min_zoom=16, zoom_start=17, max_zoom=18, name='Watercolor').add_to(m)

    m.choropleth(
        geo_data=land_parcels,
        name='Runda Parcels',
        key_on='feature.id',
        fill_color='yellow',
        # fill_color='#ffffff',
        fill_opacity='0.2',
        line_opacity='2',
        legend_name='Land parcels',
        tooltip='No Access to this information'
    )
    # dictionary that holds the style of our selected parcel shapefile
    style_parcel = {'fillcolor': '#228822', 'color': '#228822'}

    folium.plugins.MeasureControl(position='topleft', primary_length_unit='meters', secondary_length_unit='miles',
                                  primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)

    folium.features.GeoJson(parcel, style_function=lambda x: style_parcel, highlight_function=None, name='Parcels',
                            overlay=True, control=True, popup=parcel, show=True, smooth_factor=None,
                            tooltip='my parcel', embed=True).add_to(m)

    folium.plugins.Fullscreen()

    folium.LayerControl(position="topright", strings={"title": "my location", "popup": "Your position"}).add_to(m)

    folium.plugins.MousePosition(separator=':', empty_string='Unavailable', lng_first=False, num_digits=5,).add_to(m)

    folium.plugins.LocateControl().add_to(m)

    folium.plugins.MiniMap(tile_layer='OpenStreetMap', position='bottomright', width=120, height=120,
                           collapsed_width=25, collapsed_height=25, zoom_level_offset=-5, zoom_level_fixed=None,
                           center_fixed=False, zoom_animation=False, toggle_display=False,
                           auto_toggle_display=False, minimized=False, ).add_to(m)

    # folium.plugins.ScrollZoomToggler().add_to(m)

    return m
