# map_utils.py - CFipyleaflet

import ipyleaflet

DEFAULT_ICON = ipyleaflet.Icon(icon_url="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png")
SELECTED_ICON = ipyleaflet.Icon(icon_url="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png")

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
        rise_offset=200,
        icon=DEFAULT_ICON)
    if click_handler:
        marker.on_click(click_handler)
    return marker

from ipyleaflet import Icon

#default_blue = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png"
#selected_green = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png"

### Not used anymore
def make_click_handler(code, alias, map_state, info):
    def handle_click(**kwargs):
        marker = map_state["marker_dict"][code]

        if code in map_state["selected_stations"]:
            # ---- unselect ----
            map_state["selected_stations"].remove(code)
            marker.icon = Icon(icon_url=default_blue)
        else:
            # ---- select ----
            map_state["selected_stations"].append(code)
            marker.icon = Icon(icon_url=selected_green)

        # Update HTML info box
        info.value = "<b>Selected stations:</b> " + (
        	", ".join(map_state["selected_stations"])
        	if map_state["selected_stations"] else "none"
        	)

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