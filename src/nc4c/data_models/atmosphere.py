"""大气变量计算模块"""

import numpy as np
import xarray as xr


def calculate_2m_temperature(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算 2 米温度 (T2M)

    Args:
        dataset: 包含 T2M 变量的数据集

    Returns:
        温度数据数组
    """
    if "T2M" not in dataset:
        msg = "Variable T2M not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["T2M"].values,
        dims=dataset["T2M"].dims,
        coords=dataset["T2M"].coords,
    )

    return result


def calculate_u_component_wind(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算 10 米 u 分量风速

    Args:
        dataset: 包含 U10M 变量的数据集

    Returns:
        u 分量风速数据数组
    """
    if "U10M" not in dataset:
        msg = "Variable U10M not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["U10M"].values,
        dims=dataset["U10M"].dims,
        coords=dataset["U10M"].coords,
    )

    return result


def calculate_v_component_wind(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算 10 米 v 分量风速

    Args:
        dataset: 包含 V10M 变量的数据集

    Returns:
        v 分量风速数据数组
    """
    if "V10M" not in dataset:
        msg = "Variable V10M not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["V10M"].values,
        dims=dataset["V10M"].dims,
        coords=dataset["V10M"].coords,
    )

    return result


def calculate_wind_speed(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算风速 (由 u, v 分量计算)

    Args:
        dataset: 包含 U10M 和 V10M 变量的数据集

    Returns:
        风速数据数组
    """
    if "U10M" not in dataset:
        msg = "Variable U10M not found in dataset"
        raise ValueError(msg)
    if "V10M" not in dataset:
        msg = "Variable V10M not found in dataset"
        raise ValueError(msg)

    u = dataset["U10M"].values
    v = dataset["V10M"].values
    speed = np.sqrt(u**2 + v**2)

    result = xr.DataArray(
        speed,
        dims=dataset["U10M"].dims,
        coords=dataset["U10M"].coords,
    )

    return result


def calculate_total_precipitation(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算总降水量

    Args:
        dataset: 包含 PRECTOT 变量的数据集

    Returns:
        总降水量数据数组
    """
    if "PRECTOT" not in dataset:
        msg = "Variable PRECTOT not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["PRECTOT"].values,
        dims=dataset["PRECTOT"].dims,
        coords=dataset["PRECTOT"].coords,
    )

    return result


def get_atmosphere_required_variables() -> dict[str, str]:
    """
    获取大气变量计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "T2M": "2 米温度",
        "U10M": "10 米风场 u 分量",
        "V10M": "10 米风场 v 分量",
        "PRECTOT": "总降水量",
    }
