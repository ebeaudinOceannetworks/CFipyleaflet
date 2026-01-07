CFipyleaflet

Community Fishers data visualization tool.

data.py - all data loading, station info, lat/lon, and unassigned casts\
widgets.py - all ipywidgets: buttons, dropdown, text boxes\
map_utils.py - Leaflet map creation, marker creation, antpaths drawing, click handlers\
plotting.py - list of plotting functions (plotting functions are un cfplot.py)\
app.py - main script (like a rug that ties the room together), imports modules, displays widgets, display plot}

* --- Things to take care of ---
1. some .cor files have lat/lon NaN
2. some citations have multiple Communities (e.g. FORCE+Nunatsiavut+PSF) (what is FORCE?)
3. Frobisher bay stations have citations of ONC only
4. there are a lot of ONC citations around Nunatsiavut also
5. remove test harbor stations (GVHA5)