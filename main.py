# main.py - CFipyleaflet

from .cor_parser import parse_cor_folder
from .data import StationMetadata, StationData
from .map_utils import (
	create_map, 
	create_marker, 
	make_click_handler, 
	draw_transect, 
	create_base_map)
from .plotting import make_plot
from .widgets import (
    create_variable_selector,
    create_buttons,
    create_text_inputs,
    create_cor_folder_selector
)
import ipywidgets as widgets
from IPython.display import display


global metadata
metadata = []

# -----------------------
# 0. Create base map centered over Canada
# -----------------------

# Create map immediately
map_obj = create_base_map()

display(map_obj)

# create widgets
var_radio = create_variable_selector([])
go_btn, reset_btn, select_all_btn, transect_btn = create_buttons()
start_date, end_date, depths, tr_date = create_text_inputs()

# -----------------------
# 1. Ask for folder containing .cor files (stations only for now!)
# -----------------------

cor_folder_widget, load_btn, community_selector = create_cor_folder_selector()

# global
metadata = []

# -----------------------
# 2. Create map once community is selected
# -----------------------

def populate_map(map_obj, filtered_stations):
    """
    Populate map with markers for the selected stations (metadata only)
    """

    if not filtered_stations:
        print("No stations to display")
        return

    meta = StationMetadata(filtered_stations)

    lat_center = float(meta.lats.mean())
    lon_center = float(meta.lons.mean())

    # Recenter map
    map_obj.center = (lat_center, lon_center)
    map_obj.zoom = 8

    selected_stations = []
    marker_dict = {}

    # Clear existing markers if needed
    for layer in list(map_obj.layers):
        if hasattr(layer, "location"):
            map_obj.remove_layer(layer)

    # Add markers
    for code, lat, lon in zip(meta.station_codes, meta.lats, meta.lons):
        handler = make_click_handler(selected_stations, marker_dict, code)
        marker = create_marker(lat, lon, code, click_handler=handler)
        map_obj.add_layer(marker)
        marker_dict[code] = marker

# -----------------------
# 3. Define the community change callback
# -----------------------

def on_community_change(change):
    if not metadata:
        print("⚠️ Metadata not loaded yet!")
        return
    
    selected_communities = change['new']
    filtered = [
        s for s in metadata
        if (s['community'] in selected_communities) or
           (isinstance(s['community'], list) and any(c in selected_communities for c in s['community']))
    ]
    populate_map(map_obj, filtered)

# -----------------------
# 3. Define the load button callback
# -----------------------

def on_load_clicked(b):
    global metadata
    metadata = parse_cor_folder(cor_folder_widget.value)

    # Extract unique communities
    communities = set()
    for s in metadata:
        comm = s['community']
        if isinstance(comm, list):
            communities.update(comm)
        else:
            communities.add(comm)

    community_selector.options = sorted(communities)
    community_selector.disabled = False

    # Register observe now that metadata exists
    community_selector.observe(on_community_change, names='value')

# -----------------------
# 4. Link load bytton
# -----------------------
load_btn.on_click(on_load_clicked)
