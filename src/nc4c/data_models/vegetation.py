"""植被变量计算模块"""

import xarray as xr


def calculate_high_vegetation_lai(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算高植被叶面积指数 (LAIH)

    Args:
        dataset: 包含 LAIH 变量的数据集

    Returns:
        高植被叶面积指数数据数组
    """
    if "LAIH" not in dataset:
        msg = "Variable LAIH not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["LAIH"].values,
        dims=dataset["LAIH"].dims,
        coords=dataset["LAIH"].coords,
    )

    return result


def calculate_low_vegetation_lai(dataset: xr.Dataset) -> xr.DataArray:
    """
    计算低植被叶面积指数 (LAIL)

    Args:
        dataset: 包含 LAIL 变量的数据集

    Returns:
        低植被叶面积指数数据数组
    """
    if "LAIL" not in dataset:
        msg = "Variable LAIL not found in dataset"
        raise ValueError(msg)

    result = xr.DataArray(
        dataset["LAIL"].values,
        dims=dataset["LAIL"].dims,
        coords=dataset["LAIL"].coords,
    )

    return result


def get_vegetation_required_variables() -> dict[str, str]:
    """
    获取植被变量计算所需的变量映射

    Returns:
        变量名映射字典
    """
    return {
        "LAIH": "高植被叶面积指数",
        "LAIL": "低植被叶面积指数",
    }
