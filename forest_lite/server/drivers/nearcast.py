"""
Nearcast driver
"""
import datetime as dt
import os
import glob
import re
import string
from functools import lru_cache
from forest_lite.server.inject import Use
from forest_lite.server.drivers.base import BaseDriver
from pydantic import BaseModel
import pygrib as pg


class Settings(BaseModel):
    pattern: str


driver = BaseDriver()


def get_file_names():
    """Search disk for Nearcast files"""
    pattern = Settings(**driver.settings).pattern
    wildcard = string.Template(pattern).substitute(**os.environ)
    return sorted(glob.glob(wildcard))


def get_times():
    return sorted(parse_date(path) for path in get_file_names())


def parse_date(path):
    """Parse datetime from file name"""
    groups = re.search("[0-9]{8}_[0-9]{4}", os.path.basename(path))
    if groups is not None:
        return dt.datetime.strptime(groups[0], "%Y%m%d_%H%M")


@driver.override("get_times")
def nearcast_times(limits=None, times=Use(get_times)):
    return times[-limits:]


@driver.override("description")
def nearcast_description(file_names=Use(get_file_names)):
    data_vars = get_data_vars(sorted(file_names)[-1])
    return {
        "data_vars": {
            data_var: {} for data_var in data_vars
        }
    }


@lru_cache
def get_data_vars(path):
    messages = pg.open(path)
    for message in messages.select():
        yield message['name']
    messages.close()


@driver.override("tilable")
def nearcast_tilable(data_var, timestamp_ms, file_names=Use(get_file_names)):
    path = sorted(file_names)[-1]
    return get_grib2_data(path, timestamp_ms, data_var)


@lru_cache
def get_grib2_data(path, timestamp_ms, variable):
    valid_time = dt.datetime.fromtimestamp(timestamp_ms / 1000.)
    cache = {}
    messages = pg.index(path,
                        "name",
                        "scaledValueOfFirstFixedSurface",
                        "validityTime")
    if len(path) > 0:
        levels = sorted(set(get_first_fixed_surface(path, variable)))
        level = levels[0]
        times = sorted(set(get_validity(path, variable)))
        time = times[0]
        vTime = "{0:d}{1:02d}".format(time.hour, time.minute)
        field = messages.select(
            name=variable,
            scaledValueOfFirstFixedSurface=int(level),
            validityTime=vTime)[0]
        cache["longitude"] = field.latlons()[1][0,:]
        cache["latitude"] = field.latlons()[0][:,0]
        cache["values"] = field.values
        cache["units"] = field.units
        scaledLowerLevel = float(field.scaledValueOfFirstFixedSurface)
        scaleFactorLowerLevel = float(field.scaleFactorOfFirstFixedSurface)
        lowerSigmaLevel = str(round(scaledLowerLevel * 10**-scaleFactorLowerLevel, 2))
        scaledUpperLevel = float(field.scaledValueOfSecondFixedSurface)
        scaleFactorUpperLevel = float(field.scaleFactorOfSecondFixedSurface)
        upperSigmaLevel = str(round(scaledUpperLevel * 10**-scaleFactorUpperLevel, 2))
        cache['layer'] = lowerSigmaLevel+"-"+upperSigmaLevel
    messages.close()
    return cache


def get_first_fixed_surface(path, variable):
    messages = pg.index(path, "name")
    try:
        for message in messages.select(name=variable):
            yield message["scaledValueOfFirstFixedSurface"]
    except ValueError:
        # messages.select(name=variable) raises ValueError if not found
        pass
    messages.close()


def get_validity(path, variable):
    messages = pg.index(path, "name")
    try:
        for message in messages.select(name=variable):
            validTime = "{0:8d}{1:04d}".format(message["validityDate"],
                                               message["validityTime"])
            yield dt.datetime.strptime(validTime, "%Y%m%d%H%M")
    except ValueError:
        # messages.select(name=variable) raises ValueError if not found
        pass
    messages.close()
