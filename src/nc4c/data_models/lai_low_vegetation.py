"""Leaf Area Index (Low Vegetation) 计算模块"""

import xarray as xr

LAI_LV_VARIABLE: tuple[str, ...] = ("lai_lv",)


def calculate_lai_low_vegetation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = LAI_LV_VARIABLE,
) -> xr.DataArray:
    """
    获取低植被叶面积指数 (LAI)

    Args:
        dataset: 包含 lai_lv 变量的数据集
        variables: 变量名列表

    Returns:
        叶面积指数数据数组，单位 m²/m²
    """
    return dataset[variables[0]]
