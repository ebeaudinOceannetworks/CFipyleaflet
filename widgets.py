#widgets.py - CFipyleaflet

import ipywidgets as widgets
from IPython.display import display
from .cor_parser import parse_cor_folder


def create_cor_folder_selector(default_path="/Users/ebeaudin/Desktop/CF/output/"):
    global metadata

    cor_folder_widget = widgets.Text(
        value=default_path,
        description="COR Folder:",
        layout=widgets.Layout(width="500px")
    )

    load_btn = widgets.Button(description="Click here to start")

    community_selector = widgets.SelectMultiple(
        options=[],
        description="Select a community:",
        disabled=True,
        layout=widgets.Layout(width="400px", height="200px")
    )

    metadata = []
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

    load_btn.on_click(on_load_clicked)

    display(widgets.VBox([cor_folder_widget, load_btn, community_selector]))

    return cor_folder_widget, load_btn, community_selector

def create_variable_selector(var_list):
    var_radio = widgets.RadioButtons(options=var_list)
    return var_radio

def create_buttons():
    go_btn = widgets.Button(description='GO', button_style='success')
    reset_btn = widgets.Button(description='Reset', button_style='warning')
    select_all_btn = widgets.Button(description='Select All', button_style='info')
    transect_btn = widgets.Button(description='Show Transect', button_style='primary')
    return go_btn, reset_btn, select_all_btn, transect_btn

def create_text_inputs():
    start_date = widgets.Text(placeholder='YYYY-MM')
    end_date = widgets.Text(placeholder='YYYY-MM')
    depths = widgets.Text(placeholder='2,15,45')
    tr_date = widgets.Text(placeholder='YYYY-MM')
    return start_date, end_date, depths, tr_date