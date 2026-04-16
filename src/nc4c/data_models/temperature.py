"""2米温度计算模块"""

import xarray as xr

T2M_VARIABLE: tuple[str, ...] = ("t2m",)

KELVIN_TO_CELSIUS: float = 273.15


def calculate_2m_temperature(
    dataset: xr.Dataset,
    variables: tuple[str, ...] = T2M_VARIABLE,
    unit_convert: float | None = None,
) -> xr.DataArray:
    """
    计算 2 米温度 (T2M)

    将开尔文转换为摄氏度

    Args:
        dataset: 包含 t2m 变量的数据集
        variables: 变量名列表
        unit_convert: 单位转换系数，默认 K → °C (-273.15)

    Returns:
        温度数据数组，单位 °C
    """
    if unit_convert is None:
        unit_convert = KELVIN_TO_CELSIUS

    return dataset[variables[0]] - unit_convert
