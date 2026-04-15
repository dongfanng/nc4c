"""蒸发变量计算模块"""

import xarray as xr


def calculate_potential_evaporation(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算潜在蒸发量 (PEVAP)

    Args:
        dataset: 包含 PEVAP 变量的数据集

    Returns:
        潜在蒸发量数据数组
    """
    if "PEVAP" not in dataset:
        msg = "Variable PEVAP not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["PEVAP"].values,
        dims=dataset["PEVAP"].dims,
        coords=dataset["PEVAP"].coords,
    )

    return result


def calculate_evaporation(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算冠层顶部蒸发 (EVEGET)

    Args:
        dataset: 包含 EVEGET 变量的数据集

    Returns:
        冠层顶部蒸发数据数组
    """
    if "EVEGET" not in dataset:
        msg = "Variable EVEGET not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["EVEGET"].values,
        dims=dataset["EVEGET"].dims,
        coords=dataset["EVEGET"].coords,
    )

    return result


def calculate_vegetation_transpiration(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算植被蒸腾蒸发 (ETRANS)

    Args:
        dataset: 包含 ETRANS 变量的数据集

    Returns:
        植被蒸腾蒸发数据数组
    """
    if "ETRANS" not in dataset:
        msg = "Variable ETRANS not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["ETRANS"].values,
        dims=dataset["ETRANS"].dims,
        coords=dataset["ETRANS"].coords,
    )

    return result


def calculate_total_evaporation(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算总蒸发量 (EVAP)

    Args:
        dataset: 包含 EVAP 变量的数据集

    Returns:
        总蒸发量数据数组
    """
    if "EVAP" not in dataset:
        msg = "Variable EVAP not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["EVAP"].values,
        dims=dataset["EVAP"].dims,
        coords=dataset["EVAP"].coords,
    )

    return result


def get_evaporation_required_variables() -> dict[str, str]:
    """
    获取蒸发变量计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "PEVAP": "潜在蒸发量",
        "EVEGET": "冠层顶部蒸发",
        "ETRANS": "植被蒸腾蒸发",
        "EVAP": "总蒸发量",
    }
