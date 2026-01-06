# cor_parser.py

# this function is to combine all the metadata of .cor files of CF stations (!!! stations ONLY for now).

import os
from glob import glob
import re
from datetime import datetime
import numpy as np

def parse_cor_header(filepath):
    """Parse metadata from a .cor file."""
    info = {
        "deployment_count": None,
        "stationCode": None,
        "stationAlias": None,
        "lat": [],
        "lon": [],
        "deployment_times": [],
        "citation": None,
        "source_file": filepath
    }

    with open(filepath, "r", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if line.startswith("Deployment"):
                m = re.search(r"Deployment\s+(\d+)\s+of\s+(\d+)", line)
                if m:
                    info["deployment_count"] = int(m.group(2))

            elif line.startswith("Station name"):
                m = re.search(r"(CF\d+)\s+\(([^)]+)\)", line)
                if m:
                    info["stationCode"] = m.group(1)
                    info["stationAlias"] = m.group(2)

            elif line.startswith("StartDateCast"):
                time_str = (
                    line.split(":", 1)[1]
                    .replace(" ; UTC", "")
                    .strip()
                )
            
                info["deployment_times"].append(
                    datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                )

            elif line.startswith("LatitudeCastStart"):
                lat_start = float(line.split(":")[1].replace("; deg N", ""))
            elif line.startswith("LatitudeCastEnd"):
                lat_end = float(line.split(":")[1].replace("; deg N", ""))
                info["lat"].append((lat_start + lat_end) / 2)

            elif line.startswith("LongitudeCastStart"):
                lon_start = float(line.split(":")[1].replace("; deg E", ""))
            elif line.startswith("LongitudeCastEnd"):
                lon_end = float(line.split(":")[1].replace("; deg E", ""))
                info["lon"].append((lon_start + lon_end) / 2)

            elif line.startswith("Citation"):
                info["citation"] = line.replace("Citation:", "").strip()

    info["lat"] = float(np.nanmean(info["lat"])) ###non-nans only considered
    info["lon"] = float(np.nanmean(info["lon"]))

    return info

def extract_community_from_citation(citation):
    """Extract community attribution, fallback to ONC if none."""
    ONC = "Ocean Networks Canada Society"
    if not citation:
        return ONC

    attribution = citation.split(".", 1)[0]
    orgs = [o.strip() for o in attribution.split(",")]
    community_orgs = [o for o in orgs if o != ONC]

    if not community_orgs:
        return ONC
    elif len(community_orgs) == 1:
        return community_orgs[0]
    return community_orgs

def parse_cor_folder(folder, limit=None):
    """Parse all .cor files in a folder and return list of metadata dicts."""
    cor_files = glob(os.path.join(folder, "*.cor"))
    if limit:
        cor_files = cor_files[:limit]

    infos = []
    for f in cor_files:
        info = parse_cor_header(f)
        info['community'] = extract_community_from_citation(info['citation'])
        infos.append(info)
    return infos
    