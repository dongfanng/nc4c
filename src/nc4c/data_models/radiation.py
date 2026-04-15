"""辐射变量计算模块"""

import xarray as xr


def calculate_latent_heat_flux(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算地表潜热通量 (HLML)

    Args:
        dataset: 包含 HLML 变量的数据集

    Returns:
        潜热通量数据数组
    """
    if "HLML" not in dataset:
        msg = "Variable HLML not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["HLML"].values,
        dims=dataset["HLML"].dims,
        coords=dataset["HLML"].coords,
    )

    return result


def calculate_sensible_heat_flux(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算地表感热通量 (HSML)

    Args:
        dataset: 包含 HSML 变量的数据集

    Returns:
        感热通量数据数组
    """
    if "HSML" not in dataset:
        msg = "Variable HSML not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["HSML"].values,
        dims=dataset["HSML"].dims,
        coords=dataset["HSML"].coords,
    )

    return result


def get_radiation_required_variables() -> dict[str, str]:
    """
    获取辐射变量计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "HLML": "地表潜热通量",
        "HSML": "地表感热通量",
    }
