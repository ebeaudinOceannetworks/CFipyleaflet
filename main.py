# main.py - CFipyleaflet

import ipyleaflet
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import HBox, VBox

from .cor_parser import parse_cor_folder, read_cor_data
from .data import StationMetadata, StationData
from .map_utils import (
	create_map, 
	create_marker, 
	draw_transect, 
	create_base_map,
	DEFAULT_ICON,
	SELECTED_ICON)
from .plotting import make_plot
from .widgets import (
    create_variable_selector,
    create_buttons,
    create_text_inputs,
    create_cor_folder_selector
)

# -----------------------
# 0. Create base map centered over Canada
# -----------------------
global metadata
metadata = []

map_state = {
    "map_obj": create_base_map(),
    "metadata": [],
    "markers": [],
    "marker_dict": {},
    "selected_stations": [],
    "transect": None,
    "info_widget": widgets.HTML(value="<b>Selected stations:</b> none"),
    "fig_out": widgets.Output(),
    "selected_variable": None,
}

# create widgets
var_radio = create_variable_selector([])
go_btn, reset_btn, select_all_btn, transect_btn = create_buttons()
start_date, end_date, depths, tr_date = create_text_inputs()

# selected stations widget
info = widgets.HTML(value="<b>Selected stations:</b> none")

display(map_state['map_obj'])

# -----------------------
# 1. Ask for folder containing .cor files (stations only for now!)
# -----------------------

cor_folder_widget, load_btn, community_selector = create_cor_folder_selector()

# global
metadata = []

# -----------------------
# 2. Create map once community is selected
# -----------------------

def clear_map(map_obj):
    for layer in map_state["markers"]:
        map_state['map_obj'].remove_layer(layer)
    map_state["markers"].clear()

    if map_state["transect"] is not None:
        map_state['map_obj'].remove_layer(map_state["transect"])
        map_state["transect"] = None


def make_click_handler(code, alias, map_state, info):
    def handle_click(**kwargs):
        marker = map_state["marker_dict"][code]

        if code in map_state["selected_stations"]:
            map_state["selected_stations"].remove(code)
            marker.icon = DEFAULT_ICON
        else:
            map_state["selected_stations"].append(code)
            marker.icon = SELECTED_ICON

        info.value = "<b>Selected stations:</b> " + (
            ", ".join(map_state["selected_stations"])
            if map_state["selected_stations"] else "none"
        )
    return handle_click


def populate_map(filtered_stations):
    meta = StationMetadata(filtered_stations)
    
    # Clear old markers
    for m in map_state["markers"]:
        map_state["map_obj"].remove_layer(m)
    map_state["markers"].clear()
    map_state["marker_dict"].clear()
    map_state["selected_stations"].clear()
    map_state["info_widget"].value = "<b>Selected stations:</b> none"
    
    # Recenter map
    sw = (meta.lats.min(), meta.lons.min())
    ne = (meta.lats.max(), meta.lons.max())
    map_state["map_obj"].fit_bounds([sw, ne])
    
    # Add new markers
    for code, lat, lon, alias in zip(meta.station_codes, meta.lats, meta.lons, meta.alias):
    	marker = create_marker(lat, lon, code, click_handler=make_click_handler(code, alias, map_state, info))
    	map_state["map_obj"].add_layer(marker)
    	map_state["markers"].append(marker)
    	map_state["marker_dict"][code] = marker

# -----------------------
# 3. Define the community change callback
# -----------------------

def on_community_change(change):
    selected = change['new']
    filtered = [
        s for s in map_state["metadata"]
        if (s["community"] in selected) or
           (isinstance(s["community"], list) and any(c in selected for c in s["community"]))
    ]
    populate_map(filtered)

# -----------------------
# 3. Define the load button callback
# -----------------------

def on_load_clicked(b):
    map_state["metadata"] = parse_cor_folder(cor_folder_widget.value)
    
    communities = set()
    for s in map_state["metadata"]:
        comm = s["community"]
        if isinstance(comm, list):
            communities.update(comm)
        else:
            communities.add(comm)
    
    community_selector.options = sorted(communities)
    community_selector.disabled = False
    community_selector.observe(on_community_change, names='value')

# -----------------------
# 4. Link load bytton
# -----------------------
load_btn.on_click(on_load_clicked)

# -----------------------
# 5. add plotting widgets
# -----------------------
def on_go_clicked(b):
    fig_out.clear_output()
    if not selected_stations:
        with fig_out:
            print("Select at least one station.")
        return
    if selected_variable is None:
        with fig_out:
            print("Select a variable to plot.")
        return

    # Map selected_stations to files
    selected_files = [meta.files[meta.station_codes.index(code)] for code in selected_stations]

    # Plot
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6,4))

    for f in selected_files:
        df = read_cor_data(f)
        if df.empty:
            continue
        ts = df["Time"]
        data = df[selected_variable]
        station_code = f.split("/")[-1].split(".cor")[0]
        ax.plot(ts, data, label=station_code)

    ax.set_xlabel("Time")
    ax.set_ylabel(selected_variable)
    ax.legend()
    with fig_out:
        plt.show()

# HTML widget showing selected stations
info = widgets.HTML(value="<b>Selected stations:</b> none")

# GO button
go_btn = widgets.Button(description="GO", button_style='success')

# Select All / Reset buttons
select_all_btn = widgets.Button(description='Select All', button_style='info')
reset_btn = widgets.Button(description='Reset', button_style='warning')

# Handlers
def on_select_all_clicked(b):
    map_state["selected_stations"].clear()

    for code, marker in map_state["marker_dict"].items():
        map_state["selected_stations"].append(code)
        marker.icon = SELECTED_ICON

    # Update HTML info box
    info.value = "<b>Selected stations:</b> " + (
    	", ".join(map_state["selected_stations"])
    	if map_state["selected_stations"] else "none"
    	)

def on_reset_clicked(b):
    map_state["selected_stations"].clear()

    for marker in map_state["marker_dict"].values():
        marker.icon = DEFAULT_ICON

    info.value = "<b>Selected stations:</b> none"

def on_go_clicked(b):
    if not map_state["selected_stations"]:
        with fig_out:
            print("⚠️ Select at least one station")
        return

    with fig_out:
        print("Selected stations:")
        for c in map_state["selected_stations"]:
            print(f"- {c} ({map_state['aliases'][c]})")


select_all_btn.on_click(on_select_all_clicked)
reset_btn.on_click(on_reset_clicked)
go_btn.on_click(on_go_clicked)

# ------------------
# ---- display -----
# ------------------


display(VBox([
    info,
    HBox([select_all_btn, reset_btn, go_btn])
]))