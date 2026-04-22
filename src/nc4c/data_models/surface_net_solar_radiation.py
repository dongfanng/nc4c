"""表面净短波辐射数据计算模块"""

import xarray as xr

VARIABLE_NAME: tuple[str, ...] = ("ssr",)


def calculate_net_solar_radiation(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = VARIABLE_NAME,
) -> xr.DataArray:
    """
    计算表面净短波辐射数据

    Args:
        dataset: 输入数据集
        variables: 变量名列表

    Returns:
        净短波辐射数据数组，单位 J/m²（每小时的累计能量）
    """
    return dataset[variables[0]]


def get_required_variables() -> tuple[str, ...]:
    """
    获取表面净短波辐射计算所需的变量列表

    Returns:
        变量名元组
    """
    return VARIABLE_NAME
