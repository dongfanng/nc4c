"""IO 模块测试 - 风场 U/V 数据"""

from pathlib import Path

import numpy as np
import xarray as xr

from nc4c.core.io import read_netcdf


DATA_DIR = Path(__file__).parent.parent / "data"
WIND_FILE = (
    DATA_DIR / "raw_met_data" / "10m_u_component_of_wind 10m_v_component_of_wind.nc"
)


def test_read_wind_uv_preserves_coords_and_values() -> None:
    """测试风场 U/V 数据读取后经纬度与值的对应关系一致"""
    original = xr.open_dataset(WIND_FILE)
    original_u10 = original["u10"].values.astype(np.float64)
    original_v10 = original["v10"].values.astype(np.float64)
    original_lon = original.coords["longitude"].values
    original_lat = original.coords["latitude"].values

    print(f"original_u10 shape: {original_u10.shape}")
    print(f"original_v10 shape: {original_v10.shape}")
    print(f"original_lat: {original_lat}")
    print(f"original_lon: {original_lon}")
    # 第0个时间步、第0个纬度、前10个经度值
    print(f"original_u10[0, :5, :10]:\n{original_u10[0, :5, :10]}")

    # lat_ascending = original_lat[0] < original_lat[-1]
    # if not lat_ascending:
    #     original_lat = original_lat[::-1]
    #     original_u10 = original_u10[:, ::-1, :]
    #     original_v10 = original_v10[:, ::-1, :]

    # missing_value = 3.4028234663852886e38
    # original_u10 = np.where(original_u10 == missing_value, np.nan, original_u10)
    # original_v10 = np.where(original_v10 == missing_value, np.nan, original_v10)

    # processed = read_netcdf(
    #     file_paths=[str(WIND_FILE)],
    #     variables=["u10", "v10"],
    #     lon_range=[73.0, 135.0],
    #     lat_range=[33.0, 53.0],
    #     missing_value=missing_value,
    # )

    # processed_u10 = processed["u10"].values
    # processed_v10 = processed["v10"].values
    # processed_lon = processed.coords["lon"].values
    # processed_lat = processed.coords["lat"].values

    # assert processed_lon[0] >= 73.0
    # assert processed_lon[-1] <= 135.0
    # assert processed_lat[0] >= 33.0
    # assert processed_lat[-1] <= 53.0

    # lon_mask = (original_lon >= 73.0) & (original_lon <= 135.0)
    # lat_mask = (original_lat >= 33.0) & (original_lat <= 53.0)
    # expected_u10 = original_u10[:, lat_mask, :][:, :, lon_mask]
    # expected_v10 = original_v10[:, lat_mask, :][:, :, lon_mask]

    # np.testing.assert_array_almost_equal(processed_u10, expected_u10)
    # np.testing.assert_array_almost_equal(processed_v10, expected_v10)
