"""10米风速U/V分量计算模块"""

import xarray as xr

U_VARIABLE: tuple[str, ...] = ("u10",)
V_VARIABLE: tuple[str, ...] = ("v10",)


def get_u_v_arrays(
    dataset: xr.Dataset,
) -> tuple[xr.DataArray, xr.DataArray]:
    """
    获取U和V风速分量数组

    Args:
        dataset: 包含 u10/v10 变量的数据集

    Returns:
        (u_array, v_array) 元组
    """
    u_arr = dataset[U_VARIABLE[0]]
    v_arr = dataset[V_VARIABLE[0]]
    return u_arr, v_arr
