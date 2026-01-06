# map_utils.py - CFipyleaflet

import ipyleaflet

default_blue = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png"
selected_green = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png"

def create_base_map(center=(56, -96), zoom=3):
    """
    Create an empty map centered on Canada by default
    """
    return ipyleaflet.Map(
        center=center,
        zoom=zoom,
        scroll_wheel_zoom=True
    )

def create_map(center, zoom=10):
    return ipyleaflet.Map(center=center, zoom=zoom)

def create_marker(lat, lon, code, click_handler=None):
    marker = ipyleaflet.Marker(
    	location=(lat, lon),
    	title=code,
    	draggable=False,
    	rise_on_hover=True,
        rise_offset=200,)
    if click_handler:
        marker.on_click(click_handler)
    return marker

def make_click_handler(selected_stations, marker_dict, code):
    def handle_click(**kwargs):
        if code in selected_stations:
            selected_stations.remove(code)
            marker_dict[code].icon = ipyleaflet.Icon(icon_url=default_blue)
        else:
            selected_stations.append(code)
            marker_dict[code].icon = ipyleaflet.Icon(icon_url=selected_green)
    return handle_click

def draw_transect(map_obj, coords):
    if len(coords) < 2:
        return None
    transect = ipyleaflet.AntPath(
        locations=coords, dash_array=[1, 10], delay=1000,
        color='red', pulse_color='yellow', weight=5
    )
    map_obj.add_layer(transect)
    return transect