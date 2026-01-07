#data.py - CFipyleaflet

import numpy as np

class StationMetadata:
    """
    Lightweight container for station metadata only
    (used for map + selection)
    """
    def __init__(self, station_infos):
        """
        station_infos: list of dicts from parse_cor_folder
        """
        self.station_infos = station_infos

        self.station_codes = [s["stationCode"] for s in station_infos]
        self.alias = [s["stationAlias"] for s in station_infos]
        self.lats = np.array([s["lat"] for s in station_infos])
        self.lons = np.array([s["lon"] for s in station_infos])
        self.communities = [s["community"] for s in station_infos]
        self.source_files = [s["source_file"] for s in station_infos]

        # Optional
        self.deployment_times = {
            s["stationCode"]: s["deployment_times"]
            for s in station_infos
        }


class StationData:
    """
    Heavy object: loads netCDF data for plotting
    """
    def __init__(self, stationCodes, community=None):
        self.stationCodes = stationCodes
        self.community = community

        self.ds_stations = onc_cf.concatenate_stations(
            self.stationCodes,
            {"CF Community": community} if community else {}
        )

        self.lats = self.ds_stations.Latitude.values
        self.lons = self.ds_stations.Longitude.values

        self.variables = [
            var for var in self.ds_stations.data_vars
            if var not in ['Latitude', 'Longitude', 'Sound Speed',
                           'Pressure', 'Conductivity', 'alias']
        ]

