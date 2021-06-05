import folium
from folium import plugins


def color_producer(perimeter):
    if perimeter < 185:
        return 'green'
    elif 185 <= perimeter < 200:
        return 'orange'
    else:
        return 'red'


def my_map(land_parcels, parcel):
    extent = [-1.22488, 36.82467]
    m = folium.Map(location=extent, zoom_start=14, control_scale=True)
    m.choropleth(
        geo_data=land_parcels,
        name='Runda Parcels',
        key_on='gid',
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

    folium.features.GeoJson(parcel, style_function=lambda x: style_parcel, highlight_function=None, name='parcels',
                            overlay=True, control=True, popup=parcel, show=True, smooth_factor=None,
                            tooltip='my parcel', embed=True).add_to(m)

    folium.plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen',
                              force_separate_button=False)

    folium.LayerControl(position="topright",
                        strings={"title": "See you current location", "popup": "Your position"}).add_to(m)

    folium.plugins.MousePosition(position='bottomleft', separator=' : ', empty_string='Unavailable', lng_first=False,
                                 num_digits=5, prefix='', lat_formatter=None, lng_formatter=None).add_to(m)

    folium.plugins.LocateControl().add_to(m)

    folium.plugins.MiniMap(tile_layer='CartoDB dark_matter', position='bottomright', width=300, height=300,
                           collapsed_width=25, collapsed_height=25, zoom_level_offset=-5, zoom_level_fixed=None,
                           center_fixed=False, zoom_animation=False, toggle_display=False,
                           auto_toggle_display=False, minimized=False, ).add_to(m)

    folium.plugins.ScrollZoomToggler().add_to(m)

    # folium.plugins.Search(parcel, search_label=None, search_zoom=None, geom_type='Polygon', position='topleft',
    #                       placeholder='Search parcel', collapsed=False, ).add_to(m)

    # return m._repr_html_()
    # if parcel is not None:
    #     folium.features.GeoJson(parcel, style_function=None, highlight_function=None, name='parcels', overlay=True,
    #                             control=True, show=True, smooth_factor=None, tooltip=None, embed=True).add_to(m)

    return m

#
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="parcels")
# location = geolocator.geocode("175 5th Avenue NYC")
# print(location.address)
# print((location.latitude, location.longitude))
# print(location.raw)
# {'place_id': '9167009604', 'type': 'attraction', }
