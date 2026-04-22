"""土壤水分层1计算模块"""

import xarray as xr

SWVL1_VARIABLE: tuple[str, ...] = ("swvl1",)


def calculate_soil_moisture(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = SWVL1_VARIABLE,
) -> xr.DataArray:
    """
    计算土壤水分层1 (swvl1)

    直接返回原始值 (m³/m³)，无需单位转换

    Args:
        dataset: 包含 swvl1 变量的数据集
        variables: 变量名列表

    Returns:
        土壤水分数据数组，单位 m³/m³
    """
    return dataset[variables[0]]
