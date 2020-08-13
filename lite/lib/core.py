"""Example Python I/O library"""
import xarray
import numpy as np
import datetime as dt
import forest.geo


TILE_SIZE = 128


def xy_data(dataset, variable):
    """X-Y line/circle data related to a dataset"""
    # import time
    # time.sleep(5)  # Simulate expensive I/O or slow server
    if dataset == "takm4p4":
        return {
            "x": [0, 1e5, 2e5],
            "y": [0, 1e5, 2e5]
        }
    else:
        return {
            "x": [0, 1e5, 2e5],
            "y": [0, 3e5, 1e5]
        }


def get_times(dataset_name, path):
    with xarray.open_dataset(path, engine="h5netcdf") as nc:
        times = nc.time.values
    return times


def image_data(name, path, timestamp_ms, tile_size=TILE_SIZE):
    n = tile_size
    time = np.datetime64(timestamp_ms, 'ms')
    if name == "EIDA50":
        with xarray.open_dataset(path, engine="h5netcdf") as nc:
            lons = nc["longitude"].values
            lats = nc["latitude"].values
            pts = np.where(nc.time.values == time)
            if len(pts[0]) > 0:
                i = pts[0][0]
                values = nc["data"][i].values
        data = forest.geo.stretch_image(lons,
                                        lats,
                                        values,
                                        plot_width=n,
                                        plot_height=n)
        return data
    elif name == "Operational Africa":
        with xarray.open_dataset(path, engine="h5netcdf") as nc:
            lons = nc["longitude"].values
            lats = nc["latitude"].values
            values = nc["relative_humidity"][0, 0].values
        data = forest.geo.stretch_image(lons,
                                        lats,
                                        values,
                                        plot_width=n,
                                        plot_height=n)
        return data
    else:
        image = np.linspace(0, 11, n*n, dtype=np.float).reshape((n, n))
        return {
            "x": [0],
            "y": [0],
            "dw": [1e6],
            "dh": [1e6],
            "image": [
                image
            ]
        }
