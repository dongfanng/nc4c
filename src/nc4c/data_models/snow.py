"""雪深变量计算模块"""

import xarray as xr


def calculate_snow_depth(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算雪深 (SNODP)

    Args:
        dataset: 包含 SNODP 变量的数据集

    Returns:
        雪深数据数组
    """
    if "SNODP" not in dataset:
        msg = "Variable SNODP not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["SNODP"].values,
        dims=dataset["SNODP"].dims,
        coords=dataset["SNODP"].coords,
    )

    return result


def get_snow_required_variables() -> dict[str, str]:
    """
    获取雪深计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {"SNODP": "雪深"}
