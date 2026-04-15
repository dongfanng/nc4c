"""不变场数据模块"""

import xarray as xr


def get_soil_type(dataset: xr.Dataset) -> xr.DataArray:
    """
    获取土壤类型 (FRSOI)

    Args:
        dataset: 包含 FRSOI 变量的数据集

    Returns:
        土壤类型数据数组
    """
    if "FRSOI" not in dataset:
        msg = "Variable FRSOI not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["FRSOI"].values,
        dims=dataset["FRSOI"].dims,
        coords=dataset["FRSOI"].coords,
    )

    return result


def get_high_vegetation_type(dataset: xr.Dataset) -> xr.DataArray:
    """
    获取高植被类型 (VGHT)

    Args:
        dataset: 包含 VGHT 变量的数据集

    Returns:
        高植被类型数据数组
    """
    if "VGHT" not in dataset:
        msg = "Variable VGHT not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["VGHT"].values,
        dims=dataset["VGHT"].dims,
        coords=dataset["VGHT"].coords,
    )

    return result


def get_low_vegetation_type(dataset: xr.Dataset) -> xr.DataArray:
    """
    获取低植被类型 (VGLT)

    Args:
        dataset: 包含 VGLT 变量的数据集

    Returns:
        低植被类型数据数组
    """
    if "VGLT" not in dataset:
        msg = "Variable VGLT not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["VGLT"].values,
        dims=dataset["VGLT"].dims,
        coords=dataset["VGLT"].coords,
    )

    return result


def get_invariant_required_variables() -> dict[str, str]:
    """
    获取不变场计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "FRSOI": "土壤类型",
        "VGHT": "高植被类型",
        "VGLT": "低植被类型",
    }
