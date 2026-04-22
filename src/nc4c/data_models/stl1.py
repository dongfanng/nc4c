"""Soil Temperature Level 1 计算模块"""

import xarray as xr

STL1_VARIABLE: tuple[str, ...] = ("stl1",)

KELVIN_TO_CELSIUS: float = 273.15


def calculate_stl1(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = STL1_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算土壤温度 level 1

    将开尔文转换为摄氏度

    Args:
        dataset: 包含 stl1 变量的数据集
        variables: 变量名列表
        unit_convert: 单位转换系数，默认 K → °C (-273.15)

    Returns:
        土壤温度数据数组，单位 °C
    """
    if unit_convert is None:
        unit_convert = KELVIN_TO_CELSIUS

    return dataset[variables[0]] - unit_convert
