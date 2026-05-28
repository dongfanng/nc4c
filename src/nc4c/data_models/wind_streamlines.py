"""风场流线数据模型"""

import numpy as np
import xarray as xr

MISSING_VALUE = 3.4028234663852886e38


def replace_missing(data: np.ndarray) -> np.ndarray:
    data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
    mask = np.abs(data) >= MISSING_VALUE * 0.9
    data[mask] = 0.0
    return data


def get_u_v_arrays(
    dataset: xr.Dataset,
) -> tuple[xr.DataArray, xr.DataArray]:
    u_arr = dataset["u10"]
    v_arr = dataset["v10"]
    return u_arr, v_arr
