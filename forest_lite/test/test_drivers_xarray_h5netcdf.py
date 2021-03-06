from forest_lite.test.helpers import sample_h5netcdf_dim0
from forest_lite.server.drivers import xarray_h5netcdf
import pytest


@pytest.mark.skip("needs attention")
def test_dim0(tmpdir):
    path = str( tmpdir / "test-dim0.nc" )
    sample_h5netcdf_dim0(path)

    # Set up h5netcdf xarray driver
    timestamp_ms = 0
    data_var = "air_temperature"
    driver = eida50.Driver(name="dim0_dataset",
                           settings={
                               "pattern": path
                           })
    driver.data_tile(data_var, timestamp_ms, 0, 0, 0)
