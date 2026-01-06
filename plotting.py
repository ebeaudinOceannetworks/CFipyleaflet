# plotting.py - CFipyleaflet

# wrapper for cfplot functions
import cfplot

plot_dict = {
    "All Profiles": cfplot.all_profiles,
    "Profiles per Season": cfplot.seasonal_mean_profiles,
    "T-S Diagram": cfplot.TS_diagram,
    "Timeseries at Station": cfplot.timeseries_station,
    "Timeseries at Selected Depths": cfplot.timeseries_selected_depths,
    "Transect": cfplot.transect,
    "Data Availability": cfplot.data_availability,
    "Data Availability - Community": cfplot.data_availability_community,
}

def make_plot(plot_name, stations, variable, **kwargs):
    func = plot_dict.get(plot_name)
    if not func:
        raise ValueError(f"Plot {plot_name} not found")
    return func(stations, variable, **kwargs)