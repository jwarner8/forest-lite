"""Example Python I/O library"""
import glob
import xarray
import numpy as np
import datetime as dt
import forest.geo
import lib.tiling
from functools import lru_cache


TILE_SIZE = 128 # 256 # 64  # 128


def get_data_tile(pattern, data_var, timestamp_ms, z, x, y):
    path = get_path(pattern)
    return _data_tile(path, data_var, timestamp_ms, z, x, y)


@lru_cache
def _data_tile(path, data_var, timestamp_ms, z, x, y):
    time = np.datetime64(timestamp_ms, 'ms')
    zxy = (z, x, y)
    with xarray.open_dataset(path, engine="h5netcdf") as nc:

        # Find lons/lats related to data_var
        var = nc[data_var]
        for key in var.dims:
            if key.startswith("longitude"):
                lons = var[key].values
            if key.startswith("latitude"):
                lats = var[key].values

        # Filter pressure coordinate
        idx = {}
        for dim in var.dims:
            if dim.startswith("time"):
                # Search time axis
                pts = np.where(nc.time.values == time)
                if len(pts[0]) > 0:
                    i = pts[0][0]
                else:
                    # TODO: Replace with Exception
                    i = -1
                idx[dim] = i
            elif dim.startswith("pressure"):
                # Take first pressure level
                idx[dim] = 0
            elif dim.startswith("depth"):
                # Take first depth level
                idx[dim] = 0
        values = nc[data_var][idx].values
        units = nc[data_var].units

    assert values.ndim == 2, f"dims: {var.dims}"

    data = lib.tiling.data_tile(lons, lats, values, zxy,
                                tile_size=TILE_SIZE)
    data.update({
        "units": [units]
    })
    return data


def get_points(path, time):
    with xarray.open_dataset(path, engine="h5netcdf") as nc:
        pts = np.where(nc.time.values == time)
        if len(pts[0]) > 0:
            i = pts[0][0]
            data_array = nc["data"][i][::10, ::20]
    return data_array.to_dict()


def get_path(pattern):
    paths = sorted(glob.glob(pattern))
    if len(paths) > 0:
        return paths[-1]
    else:
        raise Exception(f"{pattern} path not found")


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
